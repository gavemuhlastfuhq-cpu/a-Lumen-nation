import React, { useState } from "react";
import { View, Text, Button, StyleSheet, TextInput, ScrollView, ActivityIndicator } from "react-native";
import { httpsCallable } from "firebase/functions";
import { functions } from "../services/firebaseClient";

export default function SoulContractScreen() {
  const [input, setInput] = useState("");
  const [loading, setLoading] = useState(false);
  const [result, setResult] = useState(null);

  const generate = async () => {
    setLoading(true);
    setResult(null);
    try {
      // calls the callable function 'generateSoulContract' in Firebase Functions
      const fn = httpsCallable(functions, "generateSoulContract");
      const res = await fn({ input });
      setResult(res.data || { summary: "No data returned." });
    } catch (e) {
      console.error(e);
      setResult({ error: e.message || "Function error" });
    } finally {
      setLoading(false);
    }
  };

  return (
    <ScrollView contentContainerStyle={styles.container}>
      <Text style={styles.h1}>Soul Contract</Text>
      <TextInput
        style={styles.input}
        placeholder="Paste birth data, notes, or intentions..."
        multiline
        value={input}
        onChangeText={setInput}
      />
      <View style={{ marginTop: 12 }}>
        <Button title="Generate Reading" onPress={generate} />
      </View>

      {loading && <ActivityIndicator style={{ marginTop: 12 }} />}

      {result && (
        <View style={styles.result}>
          <Text style={{ fontWeight: "700", marginBottom: 6 }}>Result</Text>
          <Text>{JSON.stringify(result, null, 2)}</Text>
        </View>
      )}
    </ScrollView>
  );
}

const styles = StyleSheet.create({
  container: { padding: 20 },
  h1: { fontSize: 22, fontWeight: "700" },
  input: { marginTop: 12, minHeight: 120, borderWidth: 1, borderColor: "#ddd", padding: 10, borderRadius: 8 },
  result: { marginTop: 16, padding: 12, backgroundColor: "#f6f6f6", borderRadius: 8 }
});
