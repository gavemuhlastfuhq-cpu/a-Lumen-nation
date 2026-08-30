import React from "react";
import { View, Text, StyleSheet } from "react-native";

export default function CodexScreen() {
  return (
    <View style={styles.container}>
      <Text style={styles.h1}>Personal Codex</Text>
      <Text style={styles.p}>List of archetypes, saved readings, and imagery assets will appear here.</Text>
    </View>
  );
}

const styles = StyleSheet.create({
  container: { flex: 1, padding: 20 },
  h1: { fontSize: 22, fontWeight: "700" },
  p: { marginTop: 10, fontSize: 16, color: "#444" }
});
