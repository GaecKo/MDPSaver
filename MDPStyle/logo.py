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

rs = Style.RESET_ALL; gr = Fore.GREEN; re = Fore.RED; cy = Fore.CYAN; wh = Fore.WHITE; bl = Fore.BLUE; ma = Fore.MAGENTA

def logo():
    return f"""
               &{cy + "&&" + rs}&&&&{wh + "#&&" + re + "&&" +wh + "%" + rs}
            .&&{cy + "&&" + rs}&&&   {wh + "&&&&" + re + "#&" + wh + "&" + rs}                             
           &&{cy + "&&" + rs}&           {wh + "&&" + re + "&&" + wh + "&" + rs}                            
           &&{cy + "&" + rs}&             {wh + "&&" + re + "%" + wh + "&" + rs}                           
          &{cy + "&#" + rs}&&             {wh + "&&&" + re + "&" + wh + "%" + rs}                           
          &&{cy + "&" + rs}&((((**(##{gr + "#" + rs}{wh + "###"+ bl + "##" + wh+"&&&" + re + "%" + rs}
        ((/(({cy + "(" + rs}((((((/ {gr + "(#" + rs}{wh + "###" + bl + "(#" + wh + "####"+ re+ "#"+ wh + "#" + rs}                        
        ({ma + "((" + rs}{cy + "((" + rs}((((#(     {gr + "#" + rs}{wh + "####" + bl + "##" + wh + "#" + re + "##" + wh + "#" + rs}   █▀▀ ▄▀█ █▀▀ █▀▀ █▄▀ █▀█ 
        ({ma + "((" + rs}(({cy + "((" + rs}/((((   {gr + "#" + rs}{wh + "###" + bl + "##" + wh + "#(#" + re + "##" + wh + "#" + rs}   █▄█ █▀█ ██▄ █▄▄ █░█ █▄█ ©
        (({ma + "((" + rs}((({cy + "((" + rs}(((   {gr + "#" + rs}{wh + "###" + bl + "##" + wh + "##" + re + "#(" + wh + "(/" + rs}                         
        ((({ma + "(" + rs}({cy + "((" + rs}((((((#{gr + "##" + rs}{wh + "##" + bl + "##" + wh + "##" + re + "##" + wh + "##" + rs}                          
         (({ma + "((" + rs}(({cy + "((" + rs}(#(({gr + "##" + rs}{wh + "##" + bl + "##" + wh + "##" + re + "##" + wh + "##" + rs}                            
            {ma + "##" + rs}  {cy + "(#" + rs}  {gr + "(/" + rs}   {bl + "((" + rs}  {re + "##" + rs}                     
   {ma + "#%   %####%" + rs}  {cy + "(#" + rs}  {gr + "(/" + rs}   {bl + "((" + rs}  {re + "%####&   %%" + rs} 
 {ma + "##  /#(" + rs}        {cy + "((" + rs}   {gr + "//" + rs}    {bl + "((" + rs}       {re + "(##  ##" + rs}                  
 {ma + "#####" + rs}        {cy + "(#" + rs}    {gr + "(/" + rs}     {bl + "((" + rs}        {re + "#####" + rs}                          
         {cy + "((# ((" + rs}    {gr + "/////" + rs}    {bl + "(( (((" + rs}                           
         {cy + ".(((((" + rs}   {gr + "//* //(" + rs}   {bl + "(((((" + rs}                           
                    {gr + "/./" + rs}
"""
