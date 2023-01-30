# author: Arthur De Neyer - GaecKo
# last update: check github (https://github.com/GaecKo/MDPSaver)
#           ==== ⚠ DISCLAIMER ⚠ ====
# This code is not suitable for professional use. As of the current state of the code, this 
# whole program is not sustainable and thus depreciated. 
# 
# If you wish to rebuilt the program, feel free to do it and I'll check the PR! 

# This code just creates the logo for the app 

from colorama import Fore, Style, init
init(autoreset=True)


def logo():
    return f"""
               &{Fore.CYAN + "&&" + Style.RESET_ALL}&&&&{Fore.WHITE + "#&&" + Fore.RED + "&&" +Fore.WHITE + "%" + Style.RESET_ALL}
            .&&{Fore.CYAN + "&&" + Style.RESET_ALL}&&&   {Fore.WHITE + "&&&&" + Fore.RED + "#&" + Fore.WHITE + "&" + Style.RESET_ALL}                             
           &&{Fore.CYAN + "&&" + Style.RESET_ALL}&           {Fore.WHITE + "&&" + Fore.RED + "&&" + Fore.WHITE + "&" + Style.RESET_ALL}                            
           &&{Fore.CYAN + "&" + Style.RESET_ALL}&             {Fore.WHITE + "&&" + Fore.RED + "%" + Fore.WHITE + "&" + Style.RESET_ALL}                           
          &{Fore.CYAN + "&#" + Style.RESET_ALL}&&             {Fore.WHITE + "&&&" + Fore.RED + "&" + Fore.WHITE + "%" + Style.RESET_ALL}                           
          &&{Fore.CYAN + "&" + Style.RESET_ALL}&((((**(##{Fore.GREEN + "#" + Style.RESET_ALL}{Fore.WHITE + "###"+ Fore.BLUE + "##" + Fore.WHITE+"&&&" + Fore.RED + "%" + Style.RESET_ALL}
        ((/(({Fore.CYAN + "(" + Style.RESET_ALL}((((((/ {Fore.GREEN + "(#" + Style.RESET_ALL}{Fore.WHITE + "###" + Fore.BLUE + "(#" + Fore.WHITE + "####"+ Fore.RED+ "#"+ Fore.WHITE + "#" + Style.RESET_ALL}                        
        ({Fore.MAGENTA + "((" + Style.RESET_ALL}{Fore.CYAN + "((" + Style.RESET_ALL}((((#(     {Fore.GREEN + "#" + Style.RESET_ALL}{Fore.WHITE + "####" + Fore.BLUE + "##" + Fore.WHITE + "#" + Fore.RED + "##" + Fore.WHITE + "#" + Style.RESET_ALL}   █▀▀ ▄▀█ █▀▀ █▀▀ █▄▀ █▀█ 
        ({Fore.MAGENTA + "((" + Style.RESET_ALL}(({Fore.CYAN + "((" + Style.RESET_ALL}/((((   {Fore.GREEN + "#" + Style.RESET_ALL}{Fore.WHITE + "###" + Fore.BLUE + "##" + Fore.WHITE + "#(#" + Fore.RED + "##" + Fore.WHITE + "#" + Style.RESET_ALL}   █▄█ █▀█ ██▄ █▄▄ █░█ █▄█ ©
        (({Fore.MAGENTA + "((" + Style.RESET_ALL}((({Fore.CYAN + "((" + Style.RESET_ALL}(((   {Fore.GREEN + "#" + Style.RESET_ALL}{Fore.WHITE + "###" + Fore.BLUE + "##" + Fore.WHITE + "##" + Fore.RED + "#(" + Fore.WHITE + "(/" + Style.RESET_ALL}                         
        ((({Fore.MAGENTA + "(" + Style.RESET_ALL}({Fore.CYAN + "((" + Style.RESET_ALL}((((((#{Fore.GREEN + "##" + Style.RESET_ALL}{Fore.WHITE + "##" + Fore.BLUE + "##" + Fore.WHITE + "##" + Fore.RED + "##" + Fore.WHITE + "##" + Style.RESET_ALL}                          
         (({Fore.MAGENTA + "((" + Style.RESET_ALL}(({Fore.CYAN + "((" + Style.RESET_ALL}(#(({Fore.GREEN + "##" + Style.RESET_ALL}{Fore.WHITE + "##" + Fore.BLUE + "##" + Fore.WHITE + "##" + Fore.RED + "##" + Fore.WHITE + "##" + Style.RESET_ALL}                            
            {Fore.MAGENTA + "##" + Style.RESET_ALL}  {Fore.CYAN + "(#" + Style.RESET_ALL}  {Fore.GREEN + "(/" + Style.RESET_ALL}   {Fore.BLUE + "((" + Style.RESET_ALL}  {Fore.RED + "##" + Style.RESET_ALL}                     
   {Fore.MAGENTA + "#%   %####%" + Style.RESET_ALL}  {Fore.CYAN + "(#" + Style.RESET_ALL}  {Fore.GREEN + "(/" + Style.RESET_ALL}   {Fore.BLUE + "((" + Style.RESET_ALL}  {Fore.RED + "%####&   %%" + Style.RESET_ALL} 
 {Fore.MAGENTA + "##  /#(" + Style.RESET_ALL}        {Fore.CYAN + "((" + Style.RESET_ALL}   {Fore.GREEN + "//" + Style.RESET_ALL}    {Fore.BLUE + "((" + Style.RESET_ALL}       {Fore.RED + "(##  ##" + Style.RESET_ALL}                  
 {Fore.MAGENTA + "#####" + Style.RESET_ALL}        {Fore.CYAN + "(#" + Style.RESET_ALL}    {Fore.GREEN + "(/" + Style.RESET_ALL}     {Fore.BLUE + "((" + Style.RESET_ALL}        {Fore.RED + "#####" + Style.RESET_ALL}                          
         {Fore.CYAN + "((# ((" + Style.RESET_ALL}    {Fore.GREEN + "/////" + Style.RESET_ALL}    {Fore.BLUE + "(( (((" + Style.RESET_ALL}                           
         {Fore.CYAN + ".(((((" + Style.RESET_ALL}   {Fore.GREEN + "//* //(" + Style.RESET_ALL}   {Fore.BLUE + "(((((" + Style.RESET_ALL}                           
                    {Fore.GREEN + "/./" + Style.RESET_ALL}
"""
