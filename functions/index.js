const functions = require("firebase-functions");
const admin = require("firebase-admin");

try {
  admin.initializeApp();
} catch (e) {
  console.log("admin init:", e.message);
}

exports.generateSoulContract = functions.https.onCall(async (data, context) => {
  // Basic safety: require authenticated user in production
  // if (!context.auth) { throw new functions.https.HttpsError('unauthenticated', 'User must be authenticated'); }

  const input = data?.input || "";
  // Placeholder AI-style processing — replace with your AI integration later
  const summary = `Placeholder reading generated for input length ${input.length}`;
  const createdAt = admin.firestore.FieldValue.serverTimestamp();

  const doc = {
    input,
    summary,
    createdAt,
    uid: context.auth?.uid || null
  };

  try {
    await admin.firestore().collection("readings").add(doc);
  } catch (e) {
    console.error("Failed to save reading:", e);
  }

  return { summary, createdAt: Date.now() };
});
