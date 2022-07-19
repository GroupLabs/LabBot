import discord
# from transformers import AutoModelForQuestionAnswering, AutoTokenizer, pipeline
from transformers import AutoModelForCausalLM, AutoTokenizer
# from transformers import pipeline
import os
from dotenv import load_dotenv

# Lite mode
# from transformers import AutoTokenizer, AutoModelForQuestionAnswering
# model_name = "deepset/roberta-base-squad2"
# nlp = pipeline('question-answering', model=model_name, tokenizer=model_name)

# tokenizer = AutoTokenizer.from_pretrained(name,)

# model = AutoModelForQuestionAnswering.from_pretrained(name)

# nlp = pipeline('question-answering', model=model_name, tokenizer=model_name)



#load_dotenv()

# TODO
# Add chat history to DialoGPT for context

## Initialize models

# Question Answering
# model_name = "deepset/roberta-base-squad2"
# nlp = pipeline('question-answering', model=model_name, tokenizer=model_name)

# Conversational
convo_tokenizer = AutoTokenizer.from_pretrained("microsoft/DialoGPT-large")
convo_model = AutoModelForCausalLM.from_pretrained("microsoft/DialoGPT-large")

# Summarizer
# summarizer = pipeline("summarization", model="facebook/bart-large-cnn")

print('Models and tokenizers successfully loaded')

# Get Discord client
client = discord.Client()

## Event Handlers

@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))
    status = "We have logged in"

@client.event
async def on_message(message):
    if message.author == client.user:
        return

    if message.content.startswith('$ping'):
        await message.channel.send('pong')
        print(message.author)
        print(message.author.name)
        print(message.author.avatar)
    
    if message.content.startswith('$help'):
        await message.channel.send('List of stable commands: ')
        await message.channel.send('COMMANDS')
        await message.channel.send('List of nightly commands: ')
        await message.channel.send('COMMANDS')

        if message.content.startswith('$q'):
            question = message.content[4::]
            if(len(question) == 0):
                await message.channel.send("I didn't get that.")
                return
            else:
                print(question)
            QA_input = {
                'question': 'Why is model conversion important?',
                'context': 'The option to convert models between FARM and transformers gives freedom to the user and let people easily switch between frameworks.'
            }
            res = nlp(QA_input)
            ans = res['answer']
            score = res['score']
            await message.channel.send(ans)
            await message.channel.send('score: ' + score)

    # if message.content.startswith('$q'):
    #     question = message.content[4::]
    #     if(len(question) == 0):
    #         await message.channel.send("I didn't get that.")
    #         return
    #     else:
    #         print(question)
    #     QA_input = {
    #         'question': 'Why is model conversion important?',
    #         'context': 'The option to convert models between FARM and transformers gives freedom to the user and let people easily switch between frameworks.'
    #     }
    #     res = nlp(QA_input)
    #     ans = res['answer']
    #     score = res['score']
    #     await message.channel.send(ans)
    #     await message.channel.send('score: ' + score)

    # if message.content.startswith('$TLDR'):
    #     query = message.content[6::]

    #     if(len(query) < 2):
    #         messages = [message.content async for message in message.channel.history(limit=30)]
    #         messages_str = ".".join(messages)
    #         summary = summarizer(messages_str, max_length=130, min_length=30, do_sample=False)
    #         await message.channel.send('Summary: ' + summary[0]['summary_text'])
    #     elif(len(query) < 35):
    #         await message.channel.send('Too short to summarize.')
    #     else:
    #         summary = summarizer(query, max_length=130, min_length=30, do_sample=False)
    #         await message.channel.send('Summary: ' + summary[0]['summary_text'])

    # if message.content.startswith('$talk'):
    #     chat = message.content[6::]
    #     if(len(chat) == 0):
    #         await message.channel.send("I didn't get that.")
    #         return
    #     else:
    #         print(chat)
        
    #     input_ids = convo_tokenizer.encode(chat + convo_tokenizer.eos_token, return_tensors='pt')
    #     return_ids = convo_model.generate(input_ids, max_length=1000, pad_token_id=convo_tokenizer.eos_token_id)
    #     response = "{}".format(convo_tokenizer.decode(return_ids[:, input_ids.shape[-1]:][0], skip_special_tokens=True))

    #     await message.channel.send(response)

client.run(str(os.environ.get('TOKEN')))
# client.run(str(os.getenv('TOKEN')))