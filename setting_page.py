import os, shutil, json, webbrowser 

settings = ("Animation Settings", "AI Personality", "Pick API Key", "About")

default_an = {
	"don't_use_animation":False,
	"delay_e_letter":0.005,
	"stop_animation":"Never"
}

default_pe = {
	"main_instruction": {
		"callme": None,
		"background": None,
	},
	"other": []
}

default_file1 = "config_animation.json"
default_file2 = "config_personal.json"



def load_setting():
	if not (os.path.exists(default_file1)
	or os.path.exists(default_file2)):
		save_setting(default_an, default_pe)
		return default_an, default_pe
	
	with open(default_file1, 'r') as file1:
		data1 = json.load(file1)
	with open(default_file2, 'r') as file2:
		data2 = json.load(file2)
		
	return data1, data2
	
def save_setting(setting1, setting2):
	with open(default_file1, 'w') as file1:
		json.dump(setting1, file1, indent=4)
		
	with open(default_file2, 'w') as file2:
		json.dump(setting2, file2, indent=4)

def clear():
	os.system('cls' if os.name == 'nt' else 'clear')
	
def termilen():
	return os.get_terminal_size().columns


def mainpage_setting():
	ter = termilen()
	
	print("-" * ter)
	
	for i, _ in enumerate(settings):
		print(f"[ {i + 1} ]: {settings[i]}")
		print("-" * ter)
		
	print("\n(S): Save\n(Q): Quit")
	
	v = input()
	
	match v:
		case '1':
			clear()
			animation_settingpage()
		case '2':
			clear()
			personality_settingpage()
		case '3':
			clear()
		case '4':
			clear()
		case _:
			clear()
			mainpage_setting()
	
def animation_settingpage():
	ter = termilen()
	s = load_setting()[0]
	
	while True:
		def d(cur):
			print('-' * ter)
			try:
				v = int(input(f"Enter new Number (Current: {cur}): "))
				if v == 0:
					return v + 0.001
				
				return v / 1000 if v > 0.01 else v
			except ValueError:
				clear()
				d(cur)
		
		def st(cur):
			print('-' * ter)
			value = input(f"Enter new Value for stop animation (Current: {cur}): ")
			
			if value.isdigit():
				return int(value)
			
			elif value == 'Never':
				return 'Never'
				
			else:
				clear()
				print("Invalid Format")
				st(s['stop_animation'])
			
		s1 = s["don't_use_animation"]
		s2 = s['delay_e_letter']
		s3 = s['stop_animation']
		
		s1 = f"Don't use Animation: [{'ON' if s1 else 'OFF'}]"
		s2 = f"Delay Each Letters: [ {s2} ]"
		s3 = f"Stop animation if chars > [ {s3} ]"
		
		lst = [s1, s2, s3]
		
		print('-' * ter)
		for i, _ in enumerate(lst):
			print(f"[ {i + 1} ]: {lst[i]}")
			print("-" * ter)
		
		print("\n(S): Save\n(Q): Quit")
		
		choice = input("\n")
		
		match choice:
			case "1":
				s["don't_use_animation"] = not s["don't_use_animation"]
				clear()
			case "2":
				clear()
				s['delay_e_letter'] = d(s['delay_e_letter'])
				clear()
			case "3":
				clear()
				s['stop_animation'] = st(s['stop_animation'])
				clear()
			
			case "S":
				clear()
				save_setting(s, load_setting()[1])
			case "Q":
				clear()
				mainpage_setting()
				return #
			case _:
				clear()

def personality_settingpage():
	ter = termilen()
	s = load_setting()[1]
	
	def main_per_setting():
		while True:
			s1 = s['main_instruction']
			s11 = s1['callme']
			
			s11 = f"(Edit) Callme: (current: {s11})"
			
			lst = [s11]
			
			print("-" * ter)
			for i, _ in enumerate(lst):
				print(f"[ {i+1} ]: {lst[i]}")
				print("-" * ter)
				
			print("\n(<): Back\n(S): Save")
			
			c = input()
			
			match c:
				case '1':
					clear()
					print('-' * ter)
					clme = input('How can AI Call you as?: ')
					
					if clme:
						s['main_instruction']['callme'] = clme
						clear()
					
					else:
						clear()
						print("Cannot adding empty str (Callme)! try again")
						main_per_setting()
						
				case '2':
					clear()

				case '<':
					clear()
					personality_settingpage()
				case 'S':
					save_setting(load_setting()[0], 
					s)
					clear()
				
				case _:
					clear()
	
	def other_per_setting():
		while True:
			ot = s['other']
			print("-" * ter)
			if ot:
				print(f"{len(ot)} Instructions")
				print("-" * ter)
				for i, _ in enumerate(ot):
					print(f"[ {i} ] instruction:\n  {ot[i]}")
					print("-" * ter)
					
			else:
				print("No Instructions\n\n")
			
			print("(i): to remove or edit instruction\n(A): to add instruction\n(S): to save instruction\n(Q): Quit")
			
			input()
			clear()
		
		
	while True:
		s1 = s['main_instruction']
		s11 = s1['callme']
		s2 = s['other']
		
		s1 = f"Main Instructions:\n       Call me as: {s11}"
		s2 = f"Other Instructions:\n{('       None' if not s2 else '\n'.join(s2))}"
		
		lst = [s1, s2]
		
		print('-' * ter)
		for i, _ in enumerate(lst):
			print(f"[ {i+1} ]: {lst[i]}")
			print('-' * ter)
			
		print("\n(S): Save\n(Q): Quit")
		
		c = input()
		
		match c:
			case '1':
				clear()
				main_per_setting()
			case '2':
				clear()
				other_per_setting()
			
			case 'S':
				save_setting(load_setting()[0], s)
			case 'Q':
				clear()
				mainpage_setting()
				return #
			case _:
				clear()
		
