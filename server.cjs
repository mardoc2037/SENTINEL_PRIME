const express = require('express');
const { exec } = require('child_process');
const cors = require('cors');
const app = express();
const port = 3001;

app.use(cors());
app.use(express.json());

app.post('/ask', (req, res) => {
  const prompt = req.body.prompt;
  const modelPath = '../models/codellama-7b-instruct.Q8_0.gguf';

  exec(`./bin/llama-cli -m ${modelPath} -p "${prompt}"`, { cwd: './build' }, (error, stdout, stderr) => {
    if (error) {
      return res.status(500).send({ error: stderr });
    }
    res.send({ response: stdout });
  });
});

app.listen(port, () => {
  console.log(`SENTINEL backend running on http://localhost:${port}`);
});
