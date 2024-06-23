const http = require('http');
const express = require('express');
const app = express();
const fs = require('fs');
const Groq = require('groq-sdk');

app.listen(3000, () => {
    console.log("Server running on port 3000");
});

const groq = new Groq({
    apiKey: "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",
    dangerouslyAllowBrowser: true,
  });

app.get("/groq", (req, res, next) => {
    const contentBuffer = streamCompletion("", groq)
    res.json({"message": contentBuffer});
});

async function readJournal() {
    return new Promise((resolve, reject) => {
        fs.readFile('journal_student.txt', 'utf8', (err, data) => {
            if (err) {
                reject(err);
            } else {
                resolve(data);
            }
        });
    });
}

async function streamCompletion(
    messages,
    groq
  ) {
    const startTime = performance.now();
    const stream = true;
    const response = await groq.chat.completions.create({
      messages: [
        {
          role: "system",
          content: `You are a helpful assistant.
          
  You are Samantha.
  
  Respond in brief natural sentences. Use tools when appropriate before giving a response. Only use a tool if it is necessary.`,
        },
        {
            role: "user",
            content: "What are you?"
        }
      ],
      model: "llama3-70b-8192",
      temperature: 0.7,
      max_tokens: 1024,
      seed: 42,
      top_p: 1,
      stream: stream,
    });
  
    let contentBuffer = "";
    if (stream) {
      // @ts-ignore
      for await (const chunk of response) {
        if (chunk.choices[0]?.delta?.content) {
          contentBuffer += chunk.choices[0]?.delta?.content;
        }
      }
    } else {
      // @ts-ignore
      contentBuffer = response.choices[0].message.content;
    }

    const endTime = performance.now();
    console.log(`[COMPLETION]: ${(endTime - startTime).toFixed(2)} ms`);
  
    
    
    return { contentBuffer };
  }

// Example usage
