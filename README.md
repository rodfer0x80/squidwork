# squidwork
<p>why work we so fly</p>

## Goals
<p> Readability</p>
<p> Ease of integration</p>
<p> Ease of expansion and development of cool assistants/bots </p>
<p> Git gud, big boi project architecture and maintenance, get programming skillz </p>
<p> Just kidding, the only goal is to impress random girls in coffee shops as apparently colourful text spam on a laptop screen isn't "attractive" - "look what my AI can do" will become the best pick up line of 2024</p>

## TODO
### Talk with VAL
[ ] move whisper template to actions call to listen and parse
[ ] move tts to actions call to talk from input
[ ] move openai whisper to tinygrad local whisper
[ ] move tts firefox to tinygrad tts (from conversation.py)
[ ] make own tinygpt or mamba? : template
[ ] move gpt/mamba template to actions brain parser? freeBing3.5 template->brain code 1 shot?
[ ] part VAL to own project depending on squidwork
[ ] document this shit on blog and stuffs? ...
### Send voice emails, social media posts/comments, texts and call VOIP extension
...
### rig giveaways to get a drone and some gpus
> https://giveaways.org/#top25
> https://upvir.al/152563/lp152563?ref_id=655ae5e672d63M
[ ] spam domain emails
[ ] open and apply to giveaway on incognito
[ ] multiprocess docker headless
...
### autoapply jobs to piss of hr ppl
[ ] smart templates for job form providers?
> https://jobs.sequoiacap.com/jobs/?skills=Artificial+Intelligence
...
### smart music assistant search and local play
...
### models
[ ] models take stdin, pass to call prompt/input_tts/input_speech in string format
[ ] add other configs in __main__ so, later we can add small logic user-side to config each model from runner file so they dont need to touch source models to config, now do the pipe logic in a couple of lines input->model->output; new models should be easy to add, just make cli model (e.g. tinygrad models are all cli models) pass args to cli call and pipe and install reqs
[ ] add requirements to install only when using specific models pip install -r requirements/gpt2.txt
[ ] add behaviours for diff models, eg get txt, speech to pass to cli models in tinygrad
