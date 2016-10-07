from utilitarian.credentials import Config

def main():
	config = Config('~/.credentials')
	print config['github'].username

if __name__ == '__main__':
	main()