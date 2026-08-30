import React from "react";
import { View, Text, Button, StyleSheet } from "react-native";

export default function HomeScreen({ navigation }) {
  return (
    <View style={styles.container}>
      <Text style={styles.title}>a-Lumen-nation</Text>
      <Text style={styles.subtitle}>Illumination • Codex • Soul-work</Text>

      <View style={styles.btnGroup}>
        <Button title="Soul Contract" onPress={() => navigation.navigate("SoulContract")} />
      </View>
      <View style={styles.btnGroup}>
        <Button title="Personal Codex" onPress={() => navigation.navigate("Codex")} />
      </View>

      <View style={styles.note}>
        <Text>Device/Dev: Termux-ready. Firebase hooked up.</Text>
      </View>
    </View>
  );
}

const styles = StyleSheet.create({
  container: { flex: 1, alignItems: "center", justifyContent: "center", padding: 20 },
  title: { fontSize: 28, fontWeight: "700", marginBottom: 6 },
  subtitle: { fontSize: 14, color: "#666", marginBottom: 20 },
  btnGroup: { width: "100%", marginVertical: 8 },
  note: { marginTop: 30, alignItems: "center" }
});
