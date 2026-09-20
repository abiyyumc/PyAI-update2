from google import genai
from google.genai.errors import APIError
import time, shutil, os, sys, re, textwrap, json
from rich.console import Console
from rich.markdown import Markdown

terminal_length = shutil.get_terminal_size().columns - 10

console = Console(width=terminal_length)

def clear():
	os.system('cls' if os.name == 'nt' else 'clear')
	
def load_setting():
	file_ani = "config_ani_se.json"
	
	with open(file_ani, "r") as file:
		return json.load(file)

def respond_md(words, prefix="AI"):
	setting = load_setting()
    
	print(f"\033[47;30m{prefix}:\033[0m ", end="", flush=True)

    # 2. Render Markdown-nya Rich
	md = Markdown(words)

    # Capture hasil render Rich
	with console.capture() as capture:
        # Pake padding (top, right, bottom, left) -> left=4 spasi biar geser masuk!
		console.print(md)

	rendered = capture.get()
    
	lines = rendered.splitlines()
	
	if len(rendered) <= 200:
		if lines:
			first_line = lines[0].lstrip()
			for char in first_line:
				sys.stdout.write(char)
				sys.stdout.flush()
				time.sleep(setting['delay_e_letter'])
			print()
	    	
			for line in lines[1:]:
				formatted_line = len(prefix + " ") + line
				for char in formatted_line:
					sys.stdout.write(char)
					sys.stdout.flush()
					time.sleep(0.005)
					print()
	            
	else:
		print(rendered)

def chat(key, model="gemini-2.5-flash"):
	client = genai.Client(api_key=key)
	chat = client.chats.create(model=model)
	
	recent = ""
	
	while True:
		try:
			user_prompt = input("\033[36mYou:\033[0m ")
			print(f"\033[1A\r\033[K{'—' * (len(user_prompt) + 4):>57}")
			print(f"{'| ' + user_prompt + '   \\':>59}")
			print(f"{'—' * (len(user_prompt) + 6):>59}\n")

			recent = user_prompt
			
			time_sent = time.strftime('%H:%M')
			if user_prompt != "$R":
				respond = chat.send_message(user_prompt)
				print()
				respond_md(respond.text)
				print()
				print(f"\033[46;34m === Sent: [{time_sent}] | $R : Resend | $Q : Quit === \033[0m")
				print()
			
		except APIError as e:
			print()
			respond_md(f"__Errno:__ {e.code} \n---\n _Message:_ {e.message}", "System")
			
			match = re.search(r"retry in ([\d\.]+)s", e.message)
			
			if match:
				delay = float(match.group(1))
				print("\033[43;31mWait for a while...\033[0m")
				time.sleep(delay)