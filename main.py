import tkinter as tk
import time


class TrieNode:
    def __init__(self):
        self.children = {}
        self.is_end_of_word = False


class Trie:
    def __init__(self, file_path):
        self.root = TrieNode()
        with open(file_path, 'r') as file:
            words = file.read().splitlines()
            for word in words:
                self.insert(word)

    def insert(self, word):
        node = self.root
        for char in word:
            if char not in node.children:
                node.children[char] = TrieNode()
            node = node.children[char]
        node.is_end_of_word = True

    def search_prefix(self, prefix):
        node = self.root
        for char in prefix:
            if char not in node.children:
                return []
            node = node.children[char]

        return self._get_words_with_prefix(node, prefix)

    def _get_words_with_prefix(self, node, current_prefix):
        result = []
        if node.is_end_of_word:
            result.append(current_prefix)

        for char, child_node in node.children.items():
            result.extend(self._get_words_with_prefix(child_node, current_prefix + char))

        return result


class NumericKeyboardApp:
    sameKeyNumber = 0
    sameKeyTime = 1000
    previousKey = "Start Of Input"
    capsOn = False

    textLeftShift = 0

    dictionary_trie = Trie("words.txt")
    recomendation_index = -1
    recommendations = []



    def __init__(self, root):
        # The initial window configuration
        self.root = root
        self.root.title("T9")
        self.root.geometry("400x300")
        self.root.resizable(width=False, height=False)

        # Number of columns = 3
        self.root.columnconfigure(0, weight=1)
        self.root.columnconfigure(1, weight=1)
        self.root.columnconfigure(2, weight=1)

        # Variable for store input
        self.text_var = tk.StringVar()

        # Variable to store the input that we will display
        self.text_var_view = tk.StringVar()

        # Create a frame with a black border for text
        text_display_frame = tk.Frame(root, bd=2, relief="solid", bg="black")
        text_display_frame.grid(row=0, column=0, columnspan=3, pady=10, padx=10, sticky="nsew")

        # Show input text inside the frame
        self.text_display = tk.Label(text_display_frame, textvariable=self.text_var_view, font=('Arial', 16),
                                     anchor="center", justify="center")
        self.text_display.pack(expand=True, fill="both")

        self.numeric_keys = {
            "1": "1.",
            "2": "2abc",
            "3": "3def",
            "4": "4ghi",
            "5": "5jkl",
            "6": "6mno",
            "7": "7pqrs",
            "8": "8tuv",
            "9": "9wxyz",
            "*": "*+",
            "0": "0 ",
            "#": "#"
        }

        # Control buttons
        self.up_button = tk.Button(root, text="↑", command=lambda: self.get_recommendations_up())
        self.up_button.grid(row=1, column=1, sticky="nsew")
        self.left_button = tk.Button(root, text="←", command=lambda: self.shift_text_left())
        self.left_button.grid(row=2, column=0, sticky="nsew")
        self.right_button = tk.Button(root, text="→", command=lambda: self.shift_text_right())
        self.right_button.grid(row=2, column=2, sticky="nsew")
        self.down_button = tk.Button(root, text="↓",command=lambda: self.get_recommendations_down())
        self.down_button.grid(row=3, column=1, sticky="nsew")

        # Show numeric keyboard
        self.one = tk.Button(root, text="1\n.", command=lambda k="1": self.print_2_letters(k))
        self.one.grid(row=4, column=0, sticky="nsew")
        self.two = tk.Button(root, text="2\nABC", command=lambda k="2": self.print_3_letters(k))
        self.two.grid(row=4, column=1, sticky="nsew")
        self.three = tk.Button(root, text="3\nDEF", command=lambda k="3": self.print_3_letters(k))
        self.three.grid(row=4, column=2, sticky="nsew")
        self.four = tk.Button(root, text="4\nGHI", command=lambda k="4": self.print_3_letters(k))
        self.four.grid(row=5, column=0, sticky="nsew")
        self.five = tk.Button(root, text="5\nJKL", command=lambda k="5": self.print_3_letters(k))
        self.five.grid(row=5, column=1, sticky="nsew")
        self.six = tk.Button(root, text="6\nMNO", command=lambda k="6": self.print_3_letters(k))
        self.six.grid(row=5, column=2, sticky="nsew")
        self.seven = tk.Button(root, text="7\nPQRS", command=lambda k="7": self.print_4_letters(k))
        self.seven.grid(row=6, column=0, sticky="nsew")
        self.eight = tk.Button(root, text="8\nTUV", command=lambda k="8": self.print_3_letters(k))
        self.eight.grid(row=6, column=1, sticky="nsew")
        self.nine = tk.Button(root, text="9\nWXYZ", command=lambda k="9": self.print_4_letters(k))
        self.nine.grid(row=6, column=2, sticky="nsew")
        self.star = tk.Button(root, text="Shift\n*+", command=lambda: self.shift())
        self.star.grid(row=7, column=0, sticky="nsew")
        self.zero = tk.Button(root, text="0\n( )", command=lambda k="0": self.print_2_letters(k))
        self.zero.grid(row=7, column=1, sticky="nsew")
        self.gridKey = tk.Button(root, text="#\n", command=lambda: self.delete_last_symbol())
        self.gridKey.grid(row=7, column=2, sticky="nsew")

    # I could create a separate function for each button, but a
    # -1 complexity in the algorithm is not worth unreadable code.
    def print_3_letters(self, key):

        current_text = self.text_var.get()

        if (self.previousKey == key and (time.time() - self.sameKeyTime) < 2):
            self.sameKeyNumber = (self.sameKeyNumber + 1) % 4
            previous_symbole = current_text[-1]
            current_text = current_text[:-1]
            if(previous_symbole.isupper()):
                current_text += self.numeric_keys[key][self.sameKeyNumber].upper()
            else:
                current_text += self.numeric_keys[key][self.sameKeyNumber]
        else:
            self.previousKey = key
            self.sameKeyNumber = 0
            if(self.capsOn):
                current_text += self.numeric_keys[key][1].upper()
                self.sameKeyNumber += 1
                self.capsOn = False
            else:
                current_text += key

        self.text_var.set(current_text)
        self.text_var_view.set(current_text[-30:])
        self.recomendation_index = -1
        self.sameKeyTime = time.time()
        self.textLeftShift = 0

    def print_4_letters(self, key):

        current_text = self.text_var.get()

        if (self.previousKey == key and (time.time() - self.sameKeyTime) < 2):
            self.sameKeyNumber = (self.sameKeyNumber + 1) % 5
            previous_symbole = current_text[-1]
            current_text = current_text[:-1]
            if(previous_symbole.isupper()):
                current_text += self.numeric_keys[key][self.sameKeyNumber].upper()
            else:
                current_text += self.numeric_keys[key][self.sameKeyNumber]
        else:
            self.sameKeyNumber = 0
            self.previousKey = key
            if(self.capsOn):
                current_text += self.numeric_keys[key][1].upper()
                self.sameKeyNumber += 1
                self.capsOn = False
            else:
                current_text += key

        self.text_var.set(current_text)
        self.text_var_view.set(current_text[-30:])
        self.recomendation_index = -1
        self.sameKeyTime = time.time()
        self.textLeftShift = 0


    def print_2_letters(self, key):

        current_text = self.text_var.get()

        if (self.previousKey == key and (time.time() - self.sameKeyTime) < 2):
            self.sameKeyNumber = (self.sameKeyNumber + 1) % 2
            current_text = current_text[:-1]
            current_text += self.numeric_keys[key][self.sameKeyNumber]
        else:
            self.previousKey = key
            self.sameKeyNumber = 0
            current_text += key

        self.text_var.set(current_text)
        self.text_var_view.set(current_text[-30:])
        self.recomendation_index = -1
        self.sameKeyTime = time.time()
        self.textLeftShift = 0
        self.capsOn = False

    def delete_last_symbol(self):

        current_text = self.text_var.get()

        self.previousKey = '#'
        self.sameKeyNumber = 0
        current_text = current_text[:-1]

        self.text_var.set(current_text)
        self.text_var_view.set(current_text[-30:])
        self.recomendation_index = -1
        self.sameKeyTime = time.time()
        self.textLeftShift = 0
        self.capsOn = False

    def shift(self):
        current_text = self.text_var.get()

        if (self.previousKey == "Shift" and (time.time() - self.sameKeyTime) < 2 and self.capsOn == False):
            self.sameKeyNumber = (self.sameKeyNumber + 1) % 2
            current_text = current_text[:-1]
            current_text += self.numeric_keys["*"][self.sameKeyNumber]
        elif (self.previousKey == "Shift" and (time.time() - self.sameKeyTime) < 2 and self.capsOn == True):
            self.sameKeyNumber = (self.sameKeyNumber + 1) % 2
            current_text += self.numeric_keys["*"][self.sameKeyNumber]
            self.capsOn = False
        else:
            self.capsOn = True
            self.previousKey = "Shift"
            self.sameKeyNumber = 0

        self.text_var.set(current_text)
        self.text_var_view.set(current_text[-30:])
        self.recomendation_index = -1
        self.sameKeyTime = time.time()
        self.textLeftShift = 0

    def shift_text_left(self):
        if ((len(self.text_var.get()) - self.textLeftShift) > 30):
            self.textLeftShift += 1
            current_text = self.text_var.get()
            if (self.textLeftShift != 0):
                self.text_var_view.set(current_text[-(30 + self.textLeftShift):-self.textLeftShift])
            else:
                self.text_var_view.set(current_text[-(30 + self.textLeftShift):0])

            self.previousKey = 'Left'
            self.capsOn = False


    def shift_text_right(self):
        if (self.textLeftShift > 0):
            self.textLeftShift -= 1
            current_text = self.text_var.get()
            if (self.textLeftShift != 0):
                self.text_var_view.set(current_text[-(30 + self.textLeftShift):-self.textLeftShift])
            else:
                self.text_var_view.set(current_text[-(30 + self.textLeftShift):])
            self.previousKey = 'Right'

    def get_recommendations_up(self):
        current_input = self.text_var.get()

        #There is nothing to search for if the user has not entered anything yet
        if(current_input==""):
            return

        #If the user scrolls through the possible options, there is no need to conduct a search again
        if self.recomendation_index == -1:
            last_word = current_input.split()[-1]  # Get last word
            first_symbole_was_upper = False
            if (last_word[0].isupper()):
                first_symbole_was_upper = True
                last_word = last_word.lower()

            #If the last character is a digit, provide all possible options for that digit
            if last_word[-1] in ['2', '3', '4', '5', '7', '8', '9']:
                self.recommendations = []
                for i in self.numeric_keys[last_word[-1]]:
                    self.recommendations.extend(self.dictionary_trie.search_prefix(last_word[:-1]+i))
            else:
                self.recommendations = self.dictionary_trie.search_prefix(last_word)

            #If we have nothing to suggest to the user, exit the function
            if(len(self.recommendations)==0):
                return
            #Allow the user to return to their initial word
            self.recomendation_index += 1
            self.recommendations.insert(0, last_word)
            if(first_symbole_was_upper):
                self.recommendations = list(map(str.capitalize, self.recommendations))

        self.recomendation_index +=1

        #If the user has viewed all possible options, we start from begin
        if (self.recomendation_index >= len(self.recommendations)):
            self.recomendation_index = 0

        #Split the input into words
        current_input_list = current_input.split()

        if len(current_input_list) > 1:
            current_input = ' '.join(current_input_list[:-1])
            current_input += (' ')
        else:
            current_input = ''

        #Add suggestion into input
        current_input += self.recommendations[self.recomendation_index]

        self.text_var.set(current_input)
        self.text_var_view.set(current_input[-30:])
        self.textLeftShift = 0
        self.capsOn = False



    def get_recommendations_down(self):
        current_input = self.text_var.get()

        #There is nothing to search for if the user has not entered anything yet
        if(current_input==""):
            return

        #If the user scrolls through the possible options, there is no need to conduct a search again
        if self.recomendation_index == -1:
            last_word = current_input.split()[-1]  # Get last word
            first_symbole_was_upper = False
            if(last_word[0].isupper()):
                first_symbole_was_upper = True
                last_word = last_word.lower()

            #If the last character is a digit, provide all possible options for that digit
            if last_word[-1] in ['2', '3', '4', '5', '7', '8', '9']:
                self.recommendations = []
                for i in self.numeric_keys[last_word[-1]]:
                    self.recommendations.extend(self.dictionary_trie.search_prefix(last_word[:-1] + i))
            else:
                self.recommendations = self.dictionary_trie.search_prefix(last_word)

            #If we have nothing to suggest to the user, exit the function
            if(len(self.recommendations)==0):
                return
            #Allow the user to return to their initial word
            self.recommendations.insert(0, last_word)
            if(first_symbole_was_upper):
                self.recommendations = list(map(str.capitalize, self.recommendations))
        self.recomendation_index -=1

        #If the user has viewed all possible options, we start from begin
        if (self.recomendation_index < 0):
            self.recomendation_index = len(self.recommendations)-1

        #Split the input into words
        current_input_list = current_input.split()

        if len(current_input_list) > 1:
            current_input = ' '.join(current_input_list[:-1])
            current_input += (' ')
        else:
            current_input = ''

        #Add suggestion into input
        current_input += self.recommendations[self.recomendation_index]

        self.text_var.set(current_input)
        self.text_var_view.set(current_input[-30:])
        self.textLeftShift = 0
        self.capsOn = False



if __name__ == '__main__':
    root = tk.Tk()
    app = NumericKeyboardApp(root)
    root.mainloop()
