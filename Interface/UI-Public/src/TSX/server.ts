import express, { Request, Response } from 'express';
import * as firebaseAdmin from 'firebase-admin';

// Initialize Firebase Admin SDK
firebaseAdmin.initializeApp({
  credential: firebaseAdmin.credential.applicationDefault(), // Use your Firebase Admin SDK credentials here
});

const app = express();
app.use(express.json());

// API route to save personalized content for a user
app.post('/saveContent', async (req: Request, res: Response) => {
  const { uid, content } = req.body;

  if (!uid || !content) {
    return res.status(400).send('Missing required fields: uid or content');
  }

  try {
    await firebaseAdmin.firestore().collection('users').doc(uid).set(
      { content },
      { merge: true }
    );
    res.status(200).send('Content saved successfully');
  } catch (error) {
    console.error('Error saving content:', error);
    res.status(500).send('Error saving content');
  }
});

// Start server
const PORT = process.env.PORT || 5000;
app.listen(PORT, () => {
  console.log(`Server running on port ${PORT}`);
});
