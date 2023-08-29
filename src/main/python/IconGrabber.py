import requests
import shutil

from PIL import Image

import pathlib

import re
from dataclasses import dataclass
from html import unescape
from random import choice
from time import sleep
from typing import Dict, Optional
from urllib.parse import unquote

import httpx
from lxml import html


REGEX_500_IN_URL = re.compile(r"[0-9]{3}-[0-9]{2}.js")
REGEX_STRIP_TAGS = re.compile("<.*?>")

USERAGENTS = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 13_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36",
]


@dataclass
class MapsResult:
    title: Optional[str] = None
    address: Optional[str] = None
    country_code: Optional[str] = None
    latitude: Optional[str] = None
    longitude: Optional[str] = None
    url: Optional[str] = None
    desc: Optional[str] = None
    phone: Optional[str] = None
    image: Optional[str] = None
    source: Optional[str] = None
    links: Optional[str] = None
    hours: Optional[Dict[str, str]] = None


class IconGrabber:
    """DuckDuckgo_search class to get search results from duckduckgo.com"""
    def __init__(
        self,
        controller,
        color=None,
        intensity=1,
        timeout=3,
    ) -> None:
        
        headers = {
            "User-Agent": choice(USERAGENTS),
            "Referer": "https://duckduckgo.com/",
        }
        self._client = httpx.Client(
            headers=headers,
            proxies=None,
            timeout=timeout,
            http2=True,
        )
        self.controller = controller
        self.icon_path = self.controller.icon_path
        self.color = color
        self.intensity = intensity

    def __exit__(self, exc_type, exc_val, exc_tb) -> None:
        self._client.close()

    def _get_url(
        self, method: str, url: str, **kwargs
    ) -> Optional[httpx._models.Response]:
        for i in range(3):
            try:
                resp = self._client.request(
                    method, url, follow_redirects=True, **kwargs
                )
                if self._is_500_in_url(str(resp.url)) or resp.status_code == 202:
                    raise httpx._exceptions.HTTPError("")
                resp.raise_for_status()
                if resp.status_code == 200:
                    return resp
            except Exception as ex:
                if i >= 2 or "418" in str(ex):
                    raise ex
            sleep(3)
        return None

    def _get_vqd(self, keywords: str) -> Optional[str]:
        """Get vqd value for a search query."""
        resp = self._get_url("POST", "https://duckduckgo.com", data={"q": keywords})
        if resp:
            for c1, c2 in (
                (b'vqd="', b'"'),
                (b"vqd=", b"&"),
                (b"vqd='", b"'"),
            ):
                try:
                    start = resp.content.index(c1) + len(c1)
                    end = resp.content.index(c2, start)
                    return resp.content[start:end].decode()
                except ValueError as e:
                    print(e)
                    pass
        return None

    def _is_500_in_url(self, url: str) -> bool:
        """something like '506-00.js' inside the url"""
        return bool(REGEX_500_IN_URL.search(url))

    def _normalize(self, raw_html: str) -> str:
        """strip HTML tags"""
        if raw_html:
            return unescape(re.sub(REGEX_STRIP_TAGS, "", raw_html))
        return ""

    def _normalize_url(self, url: str) -> str:
        """unquote url and replace spaces with '+'"""
        if url:
            return unquote(url).replace(" ", "+")
        return ""

    def images(
        self,
        keywords: str,
        region: str = "wt-wt",
        safesearch: str = "moderate",
        timelimit: Optional[str] = None,
        size: Optional[str] = None,
        color: Optional[str] = None,
        type_image: Optional[str] = None,
        layout: Optional[str] = None,
        license_image: Optional[str] = None,
    ):
        assert keywords, "keywords is mandatory"

        vqd = self._get_vqd(keywords)
        assert vqd, "error in getting vqd"

        safesearch_base = {"on": 1, "moderate": 1, "off": -1}
        timelimit = f"time:{timelimit}" if timelimit else ""
        size = f"size:{size}" if size else ""
        color = f"color:{color}" if color else ""
        type_image = f"type:{type_image}" if type_image else ""
        layout = f"layout:{layout}" if layout else ""
        license_image = f"license:{license_image}" if license_image else ""
        payload = {
            "l": region,
            "o": "json",
            "s": 0,
            "q": keywords,
            "vqd": vqd,
            "f": f"{timelimit},{size},{color},{type_image},{layout},{license_image}",
            "p": safesearch_base[safesearch.lower()],
        }

        cache = set()
        for _ in range(10):
            resp = self._get_url("GET", "https://duckduckgo.com/i.js", params=payload)
            if resp is None:
                break
            try:
                resp_json = resp.json()
            except Exception:
                break
            page_data = resp_json.get("results", None)
            if page_data is None:
                break

            result_exists = False
            res = []
            for row in page_data:
                image_url = row.get("image", None)
                if image_url and image_url not in cache:
                    
                    cache.add(image_url)
                    result_exists = True
                    res.append({
                        "title": row["title"],
                        "image": self._normalize_url(image_url),
                        "thumbnail": self._normalize_url(row["thumbnail"]),
                        "url": self._normalize_url(row["url"]),
                        "height": row["height"],
                        "width": row["width"],
                        "source": row["source"],
                    })
            next = resp_json.get("next", None)
            if next:
                payload["s"] = next.split("s=")[-1].split("&")[0]
            if next is None or result_exists is False:
                break
            return res

    def _process_request(self, query):
        try:
            ddgs_images_gen = self.images(
            query,
            region="us-en",
            safesearch="off",
            size=None,
            type_image='transparent',
            layout=None,
            license_image=None,
            )
            return ddgs_images_gen
        except Exception as e:
            print(e)
            return None
        
    def _get_image_url(self, query):
        urls = []
        return [img['image'] for img in self._process_request(f"{query} black icon png")]

    def _make_image_monochrome(self, img_path:pathlib.Path, color:str, intensity=2):
        # remove # from color
        color = color.replace("#", "")

        # open image
        image = Image.open(img_path).convert("RGBA")

        # get code to use for filter from hex code
        color =  tuple(int(color[i:i+2], 16) for i in (0, 2, 4))

        # get image size
        height, width = image.size

        print("Filtering image...")
        
        # Create a new image with RGBA mode
        new_image = Image.new("RGBA", (width, height))

        for py in range(height):
            for px in range(width):
                # Get pixel color from original image
                
                try:
                    pixel_color = image.getpixel((px, py))
                    r, g, b, alpha = pixel_color
                except:
                    r, g, b, alpha = 0, 0, 0, 0
                
                # if pixel is transparent
                if alpha == 0:
                    new_image.putpixel((px, py), (0, 0, 0, 0))
                
                # if pixel is black
                else:
                    new_image.putpixel((px, py), (color[0], color[1], color[2], alpha))
            

        # save image
        print("Saving.")
        new_image.save(img_path)


        
    
    def _save_image_from_url(self, image_urls):
        for url in image_urls:
            print(url)
            name = self.controller.generate_unique_filename()
            icon_path = self.icon_path / f"{name}.png"

            try:
                headers = {
                    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.5060.114 Safari/537.36"
                }
                # get image content
                image_content = requests.get(url, allow_redirects=True, headers=headers).content
                
                with open(icon_path, "wb") as f:
                    f.write(image_content)
                    print(f"Saved image to {icon_path} from {url}")
                return name
            except Exception as e:
                print(f"ERROR - Could not download {url} - {e}")
                return None

        return None
    
    def get_icon(self, query):
        image_urls = self._get_image_url(query)
        if image_urls:
            name = self._save_image_from_url(image_urls)
            if self.color is not None:
                self._make_image_monochrome(self.icon_path / f"{name}.png", self.color, self.intensity)

            return name
        
        return None
    
class Controller_Fake:
    def __init__(self) -> None:
        self.icon_path = pathlib.Path(__file__).parent.parent.absolute() / "resources" / "icons"
        if not self.icon_path.exists():
            self.icon_path.mkdir(parents=True)

    def generate_unique_filename(self):
        return "test"
    
    
if __name__ == "__main__":
    grabber = IconGrabber(Controller_Fake(), color="5e5e51", intensity=1)
    while True:
        print(grabber.get_icon(input("Test : ")))
