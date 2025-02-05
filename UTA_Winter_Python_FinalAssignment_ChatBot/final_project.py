from typing import List, Dict
from utils import query_llm

class Memory:
    """Stores conversation history"""
    def __init__(self):
        # Store last 3 messages (each message is a dictionary with 'role' and 'content')
        self.messages: List[Dict] = []
    
    def add_message(self, role: str, content: str) -> None:
        """
        Add a new message to memory
        Args:
            role: Either "user" or "bot" 
            content: The message content
        
        TODO:
        - Create a dictionary to store the message (hint: what two key-value pairs do you need?)
        - Add it to self.messages
        - Remember we only want to keep the last 3 messages (hint: list slicing can help here)
        """
        message = {"role": role, "content": content}
        self.messages.append(message)
        self.messages = self.messages[-3:]
    
    def get_recent_messages(self) -> str:
        """
        Get string of recent messages for context
        Returns:
            A string containing the last few messages
        
        TODO:
        - Loop through self.messages to build your output string
        - For each message, format it as "{Role}: {content}" with a newline
        - Remember to capitalize the role for readability
        - Return the final formatted string (hint: strip() can clean up extra whitespace)
        """
        output = ""
        for msg in self.messages:
            role = msg["role"].capitalize()
            content = msg["content"]
            output += f"{role}: {content}\n"
        return output.strip()

class Chatbot:
    """Base chatbot class with core functionality"""
    def __init__(self, name: str):
        self.name: str = name
        self.memory: Memory = Memory()
    
    def _create_prompt(self, user_input: str) -> str:
        """
        Create a prompt for the LLM
        Args:
            user_input: The user's message
        Returns:
            A formatted prompt string
        
        TODO: Think about:
        - What information does the LLM need to generate a good response?
        - How can you include the conversation history?
        - How should you structure the prompt to be clear?
        """
        recent_history = self.memory.get_recent_messages()
        prompt = "The following is a conversation between a user and a chatbot.\n"
        if recent_history:
            prompt += f"Conversation History:\n{recent_history}\n"
        prompt += f"User: {user_input}\nBot:"
        return prompt
    
    def generate_response(self, user_input: str) -> str:
        """
        Generate a response to user input
        Args:
            user_input: The user's message
        Returns:
            The chatbot's response
        
        TODO:
        - First store the user's message in memory (hint: which Memory method do you use?)
        - Create a prompt using your _create_prompt() method
        - Use query_llm() to get a response from GPT
        - Store the bot's response in memory before returning it
        - Make sure to handle the message storage and LLM query in the right order!
        """
        self.memory.add_message("user", user_input)
        prompt = self._create_prompt(user_input)
        response = query_llm(prompt)
        self.memory.add_message("bot", response)
        return response

class FriendlyBot(Chatbot):
    """A casual and friendly personality"""
    def _create_prompt(self, user_input: str) -> str:
        """
        Create friendly-style prompts
        
        TODO: Think about:
        - How can you make the bot sound friendly?
        - What personality traits should be included?
        - How is this different from the base chatbot?
        """
        recent_history = self.memory.get_recent_messages()
        prompt = (
            f"Hi! I'm {self.name}, your friendly assistant. I'm here to help and chat in a warm and cheerful way.\n"
        )
        if recent_history:
            prompt += f"Conversation so far:\n{recent_history}\n"
        prompt += f"User: {user_input}\n{self.name}:"
        return prompt

class TeacherBot(Chatbot):
    """A more formal, educational personality"""
    def __init__(self, name: str, subject: str):
        super().__init__(name)
        self.subject = subject
    
    def _create_prompt(self, user_input: str) -> str:
        """
        Create teaching-style prompts
        
        TODO: Consider:
        - How should an educational conversation flow?
        - How can you incorporate the subject being taught?
        - What makes a good teaching personality?
        """
        recent_history = self.memory.get_recent_messages()
        prompt = (
            f"Hello, I am Professor {self.name}, a specialist in {self.subject}. "
            "I will provide clear and thoughtful explanations to help you understand the subject matter.\n"
        )
        if recent_history:
            prompt += f"Previous conversation:\n{recent_history}\n"
        prompt += f"Student: {user_input}\nProfessor {self.name}:"
        return prompt

def main():
    """Main interaction loop"""
    # Let user choose personality
    print("Choose your chatbot:")
    print("1. Friendly Bot")
    print("2. Teacher Bot")
    
    choice = input("Enter 1 or 2: ")
    if choice == "1":
        bot = FriendlyBot("Joy")
    else:
        subject = input("What subject should I teach? ")
        bot = TeacherBot("Prof. Smith", subject)
    
    print(f"\n{bot.name}: Hello! How can I help you today?")
    
    while True:
        user_input = input("You: ").strip()
        if user_input.lower() == "quit":
            break
        
        response = bot.generate_response(user_input)
        print(f"{bot.name}: {response}")

if __name__ == "__main__":
    main()