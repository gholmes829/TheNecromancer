import os
import json
from text import Text
from typing import List, Dict, Tuple
from tqdm import tqdm
import matplotlib.pyplot as plt 
import multiprocessing as mp 
import time 
import numpy as np

class CorpusInterface:
    def __init__(self) -> None:
        self.paths = {}
        self.paths["current"]   = os.getcwd()
        self.paths["corpora"]   = os.path.join(self.paths["current"], "corpora")
        self.paths["figures"]   = os.path.join(self.paths["current"], "figures")

        # list of methods that user will be able to choose from 
        self.modes = [
            #("Generate Wordclouds",    self.generate_wordclouds),
            ("Print Corpus Contents",  self.print_corpus_info),
            ("Documents by Decade", self.plot_documents_by_decade)
        ]

    def run(self) -> None:
        while True:
            mode = self.select_mode()
            if mode is None: break
            mode()
        return


    # ----------------------------------------------
    #              Analysis Methods
    #-----------------------------------------------

    def generate_wordclouds(self):
        """
        Generates wordclouds for each text in a given corpus
        Saves to Figures/<corpus>/wordclouds/
        Multiprocessed

        """
        corpus, name = self.select_corpus()
        if corpus is None: return 

        save_path = self.get_path([self.paths['figures'], name, 'wordclouds'])
        paths = [os.path.join(save_path, text.title + ".png") for text in corpus]
        args = list(zip(corpus, paths)) 

        print("Generating wordclouds...")
        with mp.Pool(processes = 4) as p:
            list(tqdm(p.imap_unordered(self.generate_wordcloud_work, args), total = len(args)))

    def plot_documents_by_decade(self):
        corpus, name = self.select_corpus()
        if corpus is None: return

        years = [doc.year for doc in corpus]
        minimum = 1720
        maximum = 1890
        bins = 18

        with plt.style.context('Solarize_Light2'):
            fig = plt.figure(figsize = (12, 8))
            plt.rcParams.update({
                'font.family': 'serif',
                'font.size': 12
            })
            plt.hist(years, bins=range(1720, 1900, 10), align='mid', color='goldenrod')
            plt.title(f"Documents in {name} Corpus by Decade")
            plt.show()
            plt.close()

    # ----------------------------------------------
    #              Utility Methods
    #-----------------------------------------------

    def generate_wordcloud_work(self, args: Tuple[Text, str]):
        """
        Helper function called by generate_wordclouds
        Plots the wordcloud image with matplotlib and saves
        
        """
        text, path = args
        fig = plt.figure()
        plt.imshow(text.generate_wordcloud(
            stopwords = settings.stopwords,
            size = (600, 600)),
            interpolation = 'bilinear',
            cmap = 'Paired'
        )
        plt.axis('off')
        plt.savefig(path)
        plt.close(fig)

    def print_corpus_info(self):
        """
        Prints the author, year, and title for each work in a corpus

        """
        corpus, name = self.select_corpus()
        if corpus is None: return 

        print(f"\n{name} Texts: ")
        for text in corpus:
            print('-' * 50)
            print(text.get_info())
        print('\n\n')

    def retrieve_texts(self, info: Dict[str, any], path: str) -> List[Text]:
        """
        Reads an 'info.json' file and returns a list of Text objects

        """
        texts = []
        for entry in info: # iterate through all the texts contained in the 'info' dictionary
            texts.append(Text(path, **entry))
        texts.sort(key = lambda t: t.year) # sort texts by year (ascending)
        return texts

    def get_path(self, path_list: List[str]) -> str: 
        """
        Checks if the path from the beginning to end of the list exists
        If so, return that path
        If not, create that path and then return it

        Used for saving figures (e.g., wordclouds, graphs, etc.)

        """
        path = path_list[0]
        for i in range(1, len(path_list)):
            new_path = os.path.join(path, path_list[i])
            if not os.path.exists(new_path): os.mkdir(new_path)
            path = new_path 
        return path 
    
    def read_corpus(self, corpus_path: str) -> List[Text]:
        with open(os.path.join(corpus_path, 'info.json')) as infile: info = json.load(infile) 
        return self.retrieve_texts(info, corpus_path)

    def get_corpus(self, corpus_path, min_year = -float('inf'), max_year = float('inf')) -> list[Text]:
        texts = self.read_corpus(corpus_path)
        return [t for t in texts if t.year >= min_year and t.year <= max_year]
        

    # ----------------------------------------------
    #                UI Methods
    #-----------------------------------------------

    def select_mode(self):
        """
        Choose type of analysis

        """
        num_modes = len(self.modes)
        msg = "Action:\n" 
        for i, mode in enumerate(self.modes, start = 1): # list the modes
            msg += f"   {i}) {mode[0]}\n"
        msg += f"   {num_modes + 1}) Exit" 
        choice = self.getValidInput(msg, dtype = int, valid=range(1, num_modes + 2)) - 1 # let user choose mode
        if (choice != num_modes):
            return self.modes[choice][1] # return the method associated with the chosen mode
        return None # user has chosen to leave the program

    def select_corpus(self) -> (List[Text], str): 
        """
        Returns a list of texts for a chosen corpus as well as the corpus' name

        """
        corpora: List[str] = os.listdir(path = self.paths['corpora']) # retrieve list of subdirectories in corpora directory
        num_corpora = len(corpora)
        msg = "Select Corpus:\n"
        for i, corpus in enumerate(corpora, start = 1): # list corpora for user to choose from
            msg += f"   {i}) {corpus}\n"
        msg += f"   {num_corpora + 1}) Back"
        choice = self.getValidInput(msg, dtype = int, valid = range(1, num_corpora + 2)) - 1
        if choice != num_corpora:
            corpus_path = os.path.join(self.paths['corpora'], corpora[choice]) # find info.json
            corpus = self.read_corpus(corpus_path)
            return corpus, corpora[choice]

            # # open info.json and read its contents into 'info'
            # with open(os.path.join(corpus_path, 'info.json')) as infile: info = json.load(infile) 
            # return self.retrieve_texts(info, corpus_path), corpora[choice]
        return None # user has chosen to go back

    @staticmethod
    def getValidInput(
				  msg: str,
				  dtype: any = str,
				  lower: float = None, upper: float = None,
				  valid: set = None,
				  isValid: callable = None,
				  end=None
				  ) -> any:
        print(msg)
        while True:
            try:
                choice = dtype(input("\nChoice: "))
            except ValueError:  # if type can't be properly converted into dtype
                continue
            if (lower is None or choice >= lower) and \
                    (upper is None or choice <= upper) and \
                    (valid is None or choice in valid) and \
                    (isValid is None or isValid(choice)):
                if end is not None:
                    print("", end=end)
                return choice


            
