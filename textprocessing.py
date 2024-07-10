class TextProcessing:
    def __init__(self, client):
        self.client = client
    
    def text_gpt_update(self, text):
        
        # use gpt model improve dialogs quality (remove wrong symbols or put missing)
        
        completion = self.client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
              {"role": "system", "content": "You are a scraped text to dialog converter."},
              {"role": "user", "content": "Convert scraped text - {} into normal dialog, removing or replacing wrong symbols, non-english words. Return it in JSON format. Remove all '\n' symbols.".format(text)}
            ]
        )

        dialog = completion.choices[0].message.content
        fixed = dialog.replace("\n", "")
        result = json.loads(fixed)
        return result

    def get_unique_speakers(self, res):
        
        # find unique speakers of conversation
        
        for key in res.keys():
            speaker_list = list(set([x['speaker'] for x in res[key]]))
            break
            
        return speaker_list