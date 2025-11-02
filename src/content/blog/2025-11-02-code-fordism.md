---
title: Code fordism
description: ...how Claude Code is streamlining my output
date: 2025-11-02T00:11:00Z
tags: ["software", "AI"]
draft: false
---

> [!NOTE]
> I spent way too much time this morning gathering my thoughts on the impact of AI on my development workflow. In the end, here's what I want to say that hasn't been said already a million times.

## Some change you resist, some you're late to embrace
Everyday there's a new app, framework, language, workflow, mindset that comes out. If you pick up on everything, you don't have time for anything else. If you resist everything, you'll miss crucial chances to upskill. Like a colleague I once said who was still pining for the good old days of writing COBOL.

AI-centric workflows to "traditional" software development start to feel like Amazon to physical stores, or AWS to self-owned infrastructure, for that matter. Sure, sometimes you prefer or even need the human element in your shopping experience; now and then it's just easier to spin something up in your Raspberry Pi rather than set up some remote infrastructure. But for many use cases online shopping and remote infrastructure is just a better and smoother experience.

Same with AI in the software development process. Imagine we were moving in the opposite direction: as we were used to AI-agentic workflows, new solutions popped up that required us to adapt, to plan and solve every requirement to the most minute detail relying solely on our knowledge and online (non-AI) information. I doubt we'd be eager to make that move.

## We won't have fewer engineers, just fewer developers
Some project a future where non-tech people will just use AI directly instead of relying on engineers. I doubt that, at least in the next 10 years. For one thing, the tech isn't there yet. It can't translate high and complex level requirements into a solution, and iterate with absolute autonomy; but also, this would require a cultural shift: a good AI user needs an analytical mindset *(not exclusively, but certainly for software development work)*, a strong tech background, and time.

Sure, if your product is some database wrapper like a simple inventory management system, AI might set this up quickly and well enough to minimise the need for engineering oversight. This is an issue for *developers*, but not so much for *engineers*.

If I'm allowed a paragraph to be pedantic on linguistics and reductive on the demographics of the tech industry, I associate the term *developer* to a tech enthusiast that has a practical knowledge of software development; and *engineer* suggest to me someone who, in addition to that, also has a critical thinking mindset and a deep theoretic knowledges of computer systems.

Whether one agrees with these monikers, let's use them for now. It's pretty evident not only will developers struggle sooner than engineers with AI advancements, it's probably a good thing. In the same way that many technological advances in the last 200 years have rendered a lot of jobs obsolete. It sucks and feels wrong to say it, especially as I'm writing about upgrading my workflow to rely more on AI, but I think that's true. Engineers will just transition to a more managerial role - especially as AI agents already behave like junior and mid-level engineers.

> [!IMPORTANT] 
> The big difference is the skillset needed to thrive. The focus is more than ever on **critical thinking** and **computer system theory**.  You don't need to rely so heavily on your knowledge of a language, tool, or framework.

As AI does more and more of the development grunt work, debugging skills become more and more important. No surprise that quickly finding and fixing bugs relies heavily on critical thinking and a solid theoretical knowledge. As Jonathan Blow indicates in the X thread below, debugging is a crucial skill for an engineer.

<blockquote class="twitter-tweet"><p lang="en" dir="ltr">Dude the very very hardest problems I have debugged took 2 days, and I haven&#39;t had anything that took that long in about 20 years because I got better at programming and debugging. If you are spending a week on a small set of &#39;if&#39; statements, mega omega red flag.</p>&mdash; Jonathan Blow (@Jonathan_Blow) <a href="https://twitter.com/Jonathan_Blow/status/1981027925542486291?ref_src=twsrc%5Etfw">October 22, 2025</a></blockquote> <script async src="https://platform.twitter.com/widgets.js" charset="utf-8"></script>

## Don't go down a rabbit hole
I saw an experienced web3 developer the other day streaming with Claude Code, and thought I'd give it a try. What followed was a significant paradigm shift in my development workflow (hence this post). I just started trying this out, but these are my early conclusions:
1. There's no one-size-fits-all. Working closely with and delegating to an AI assistant will probably be the norm within the next year or so, but this can take many forms
2. It's very easy to go overboard. MCPs, for example, can easily bloat the Claude Code context, and degrade results. I stuck with just a couple for now. But there's also complex 3rd-party solutions for huge workflow orchestration, and all, which I'm not that interested in at the moment. First, I need to have a clearer sense of the kinds of things that Claude Code will save me time with
3. This is incredible for quickly bootstrapping projects, and saving time with dull work. Creating repos, issues, PRs, moving files around, adding new files with boilerplate code, writing basic tests, etc.
4. For larger codebases, very complex solutions, limited access rights, and/or large teams that require closer collaboration, the impact is more limited.

If you **do** want to go down a rabbit hole, check out [this video](https://www.youtube.com/watch?v=amEUIuBKwvg) and [this list](https://www.youtube.com/watch?v=SUysp3sJHbA&list=PL4cUxeGkcC9g4YJeBqChhFJwKQ9TRiivY&index=1)!

## How it's changed for me
As of now, my workflow for small personal projects went from
1. **document:** document feature ideas and system design in a notebook or Notion page
2. **create tickets:** distribute tasks into small tickets
3. **implement:** in a feature/hotfix branch
4. **commit:** frequently - I usually have a simple pre-commit hook for linting, static analysis, and simple checks
5. **merge:** to main branch when done
6. **CI/CD:** *very rarely*, I'll have some pipeline in the repository to build and run tests. But honestly test coverage is pretty low in these projects where I'm just exploring some new tech or idea.

to

1. I run a command to create a project based on my idea, system preferences, constraints, and Claude Code creates a GitHub repository and sets up the appropriate CI/CD
2. For new features or bugs I run a command (on Claude Code in my VSCode) to create an issue with a name and a description. Claude Code will
    
    a. Create a GitHub issue
    
    b. Go to a feature/fix branch
    
    c. Implement a solution
    
    d. Run tests, and iterate on the solution as necessary to pass the tests
    
    e. Create a PR
    
    f. Link the GitHub issue and the PR together
    
    g. Issue a code review
    
    h. Send me a report

Along the way, it will ask for my input and I will supervise and correct its thought process. When everything is to my satisfaction, I merge the PR.

> [!IMPORTANT]
> This isn't the 10x engineer meme! I don't just let Claude run rampant in my code base. It's important for me to still be intricately aware of the implementation details, so that I can evaluate future changes or bugs critically. It's not about swapping some good output for three times more garbage. If I can't keep up with what Claude is doing under the hood, that's a problem. It's about not having to manually do it if it can be avoided and remembering or looking up extensive syntax if I can focus on other things.

<img src="/2025-11-02-code-fordism/10x_engineer_superman.png" alt="10x engineer superman" style="width: 30%; max-width: 300px;">

This unblocks me to work on multiple issues at a time, one in each Claude Code session. As a side note, since my contribution is now much more conversational, I'm trying out interacting with Claude Code with speech-to-text. So far, I've had mixed results because a lot of the code specific terms are misunderstood, and I have to go back and forth to fix prompts. But maybe I'll get better as I practice, or I find some open source tool that is tailored to this.

## Parting thoughts
The new workflow seems promising. Yesterday, I moved my blog from my Gitlab account to Github (something I'd been meaning to do for a while) in a few minutes. All the while I was working on a new proof-of-concept for a dapp. There are certainly hiccups along the way: the text-to-speech inaccuracies I mentioned earlier, the fact that Claude keeps asking for permissions for trivial stuff (I think I got that sorted for the most part now), the occasional sneaky inaccuracy or change that I didn't request. A small cost of the efficiency gains. It really does feel like *code Fordism*, only the factory produces code instead of cars.

And if in a few weeks I decide it wasn't worth it, it will at least be a good exercise in high-level thinking and system design. 

As a former colleague used to say:
> "One may spend a week working through a pointless feature to save an hour in planning."

Maybe a modern version would be:
> "One may spend a day implementing a feature to avoid running an AI workflow in five minutes."

## Bonus
As proof that AI isn't there yet, here's the png I used to generate the 10x engineer image, and the first result I got, with the prompt *"Redraw this. It should EXACTLY identical to the original, except: 1. In the last image of the middle row, replace "It's ... !" with "It's a 10x engineer!" 2. Replace the plane and the parrot in the bottom row image with an engineer"*:

<div style="display: flex; gap: 20px;">
    <img src="/2025-11-02-code-fordism/10x_engineer_original.png" alt="Original image" style="width: 25%;">
    <img src="/2025-11-02-code-fordism/10x_engineer_first_result.png" alt="First result" style="width: 25%;">
</div>
