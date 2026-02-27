import os
import sys
import subprocess
import json
import readline

class AdenHiveCLI:
    def __init__(self):
        self.prompt = "\033[92mAdenHive>\033[0m "
        self.agent_name = os.environ.get("ADEN_DEFAULT_AGENT", "sales_agent") # Example default
        self.history_file = os.path.expanduser("~/.aden_hive_history")

    def setup_readline(self):
        try:
            readline.read_history_file(self.history_file)
        except FileNotFoundError:
            pass
        import atexit
        atexit.register(readline.write_history_file, self.history_file)

    def run_agent(self, prompt_text):
        env = os.environ.copy()
        env["PYTHONPATH"] = f"{env.get('PYTHONPATH', '')}:core:exports"
        
        # We construct the input JSON payload
        input_data = json.dumps({"prompt": prompt_text})
        
        cmd = [sys.executable, "-m", self.agent_name, "run", "--input", input_data]
        
        print(f"\033[93m[System]\033[0m Dispatching to agent '{self.agent_name}'...")
        try:
            # We run it and stream the output back to the terminal
            result = subprocess.run(cmd, env=env, text=True, capture_output=True)
            if result.returncode == 0:
                print(f"\033[96m[Agent Response]\033[0m\n{result.stdout}")
            else:
                print(f"\033[91m[Agent Error]\033[0m\n{result.stderr}")
        except Exception as e:
            print(f"\033[91m[Error]\033[0m Failed to execute agent: {e}")

    def loop(self):
        print("\033[1m=== Aden Hive CLI Chatbot ===\033[0m")
        print("Type your message to send it to the agent. Type 'exit' or 'quit' to quit.")
        print("Type '/agent <name>' to switch the active agent.")
        print("-" * 40)
        
        self.setup_readline()

        while True:
            try:
                user_input = input(self.prompt).strip()
                if not user_input:
                    continue
                if user_input.lower() in ['exit', 'quit']:
                    break
                if user_input.startswith('/agent '):
                    self.agent_name = user_input.split(' ', 1)[1].strip()
                    print(f"\033[94m[System]\033[0m Switched active agent to: {self.agent_name}")
                    continue
                
                self.run_agent(user_input)
                
            except (KeyboardInterrupt, EOFError):
                print("\nExiting...")
                break

if __name__ == "__main__":
    cli = AdenHiveCLI()
    cli.loop()
