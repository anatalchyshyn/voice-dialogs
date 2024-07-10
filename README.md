# PDF dialogs to mp3 speech

This repository provide helpfull tool to transform pdf scans of dialogs (for example from English Textbooks) to mp3 conversation with choosen voices.

### Steps

1. Split pdf file into the pages. If the dialog saved not as image but as text just skip the second step.
2. Extract text from image.
3. Use gpt technology to improve text quality (add missing elements, remove wrong ones) and rebuild it in JSON format.
4. Choose the voices, that should be used for lines.
5. Make line by line and them combine them all together

### Colab

You can also text in colab notebook over here - https://colab.research.google.com/drive/1vaZ36L8sp_IJfrPUdn_ykp-cKZI1npfI?usp=sharing
