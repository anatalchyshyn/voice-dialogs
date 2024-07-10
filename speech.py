class SpeechModel:
    def __init__(self):
        
        self.processor = None
        self.model = None
        self.vocoder = None
        self.embeddings_dataset = None
        self.interval_ms = 1000
    
    def upload_model(self):
        
        # download speech model
        
        device = "cuda" if torch.cuda.is_available() else "cpu"
        self.processor = SpeechT5Processor.from_pretrained("microsoft/speecht5_tts")
        self.model = SpeechT5ForTextToSpeech.from_pretrained("microsoft/speecht5_tts").to(device)
        self.vocoder = SpeechT5HifiGan.from_pretrained("microsoft/speecht5_hifigan").to(device)
        self.embeddings_dataset = load_dataset("Matthijs/cmu-arctic-xvectors", split="validation")
        
        
    def save_text_to_speech(self, text, output_filename, speaker=None):
    
        # get speech and save it
    
        inputs = processor(text=text, return_tensors="pt").to(device)
        if speaker is not None:
            speaker_embeddings = torch.tensor(embeddings_dataset[speaker]["xvector"]).unsqueeze(0).to(device)
        else:
            speaker_embeddings = torch.randn((1, 512)).to(device)
        speech = model.generate_speech(inputs["input_ids"], speaker_embeddings, vocoder=vocoder)
        sf.write(output_filename, speech.cpu().numpy(), samplerate=16000)
        return output_filename
    
    def combine_replics(self, mp3_files, voice_folder, file_name):
        
        # combine replics into dialog
        
        combined_audio = AudioSegment.from_mp3(os.path.join(voice_folder, mp3_files[0]))

        for file in mp3_files[1:]:
            audio_segment = AudioSegment.from_mp3(os.path.join(voice_folder, file))
            combined_audio = combined_audio + AudioSegment.silent(duration=self.interval_ms) + audio_segment
        combined_audio.export(os.path.join(voice_folder, file_name), format="mp3")
