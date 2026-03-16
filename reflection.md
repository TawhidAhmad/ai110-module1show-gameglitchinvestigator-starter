# 💭 Reflection: Game Glitch Investigator

Answer each question in 3 to 5 sentences. Be specific and honest about what actually happened while you worked. This is about your process, not trying to sound perfect.

## 1. What was broken when you started?

- What did the game look like the first time you ran it?

It looked like basic Streamlit UI with the main interface on the right and settings on the left.

- List at least two concrete bugs you noticed at the start  
  (for example: "the secret number kept changing" or "the hints were backwards").

- The secret did not change depending on the difficulty level. At times this resulted in a secret higher than the range identified. For example the secret was 95 while the Difficulty was Easy (Range:1-20)
- The Higher and Lower logic does not work. For example the secret is 95 and I guess 20 and it says goes higher but it continues to always say go higher even if I give a guess like 100 
- It allows me to input numbers outside of the range in the difficulty, practically it should not allow me to input such numbers. 
- Normal and Hard ranges should be switched. 
- Developer Debug info is incorrect except the secret. 

---

## 2. How did you use AI as a teammate?

- Which AI tools did you use on this project (for example: ChatGPT, Gemini, Copilot)?
Claude Code
- Give one example of an AI suggestion that was correct (including what the AI suggested and how you verified the result).
That the higher and lower logic was flipped, I didn't initially realize that was the case.
- Give one example of an AI suggestion that was incorrect or misleading (including what the AI suggested and how you verified the result).
The tests were not correctly running when using pytest which I had to figure why. 

---

## 3. Debugging and testing your fixes

- How did you decide whether a bug was really fixed?
 By playing the game and seeing if it correctly fixed. 
- Describe at least one test you ran (manual or using pytest) and what it showed you about your code.
Inputting a nuber outside of the range and it showed that it accuruately showed to input a new guess without affecting guess count. 
- Did AI help you design or understand any tests? How?
One of the test I did not initially think to input a null number but AI was able to create that test case. 

---

## 4. What did you learn about Streamlit and state?

- In your own words, explain why the secret number kept changing in the original app.
Every time a user interacted with the app Streamlit re-ran the entire script from top to bottom, which caused random.randint() to generate a brand new secret number on each rerun.
- How would you explain Streamlit "reruns" and session state to a friend who has never used Streamlit?
Imagine every time you clicked anything on a webpage, the whole page refreshed and forgot everything you were doing on the site.
- What change did you make that finally gave the game a stable secret number?
I used st.session_state to store the secret number the first time it was generated, so instead of calling random.randint() every rerun, the app checks if a secret already exists.

---

## 5. Looking ahead: your developer habits

- What is one habit or strategy from this project that you want to reuse in future labs or projects?
 - This could be a testing habit, a prompting strategy, or a way you used Git.
Generating a pytest file, would be amazing to reuse to make evals quickly. 
- What is one thing you would do differently next time you work with AI on a coding task?
It to input the comments for FIXs rather than me typing it out. 
- In one or two sentences, describe how this project changed the way you think about AI generated code.
It isn't just for generating code from blank but can actually come to fix bugs in previously developed project and call out bugs as well. 