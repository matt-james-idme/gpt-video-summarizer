# YouTube Video Summarizer with GPT-3

This Python script allows you to extract video summaries and major themes/points from YouTube videos using the GPT-3 language model. It leverages the `youtube_transcript_api` library to retrieve video transcripts and OpenAI's GPT-3 API for natural language processing.

## Prerequisites

Before you can use this script, you'll need the following:

1. An OpenAI GPT-3 API key. You can obtain an API key by signing up for an account on the OpenAI platform.
2. Python 3 installed on your system.
3. The `youtube_transcript_api` Python library, which can be installed using `pip`:

```
pip install youtube-transcript-api
```
   
5. The `openai` Python library, which can be installed using `pip`:

```
pip install openai
```

## Usage

1. Clone this repository to your local machine: git clone https://github.com/clorth0/gpt-video-summarizer.git

```
cd gpt-video-summarizer
```
   
2. Set your OpenAI API key as an environment variable by either exporting it or adding it to a `.env` file in the project directory:

```
export OPENAI_API_KEY=your-api-key
```

...or create a `.env` file with the following content: 

'''
OPENAI_API_KEY=your-api-key
'''

3. Run the script by executing:

```
python3 transcribe.py
```

4. You'll be prompted to enter the YouTube Video ID (the alphanumeric code in the video's URL) for the video you want to summarize.

5. The script will retrieve the video transcript, generate a summary, and provide a list of major themes/points discussed in the video.

6. Review the generated output in the terminal.

## Customization

You can customize the behavior of the script by modifying the code in `transcribe.py`. You can adjust parameters such as the maximum token limit and temperature for the GPT-3 model, or change the prompt to better suit your needs.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Acknowledgments

- [Daniel Miessler](https://twitter.com/DanielMiessler) for inspiring the project with his own.
- [OpenAI](https://openai.com) for providing the GPT-3 API.
- [youtube_transcript_api](https://github.com/jdepoix/youtube-transcript-api) for the YouTube transcript retrieval.

Feel free to contribute to this project or report any issues you encounter. Happy summarizing!
