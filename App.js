import React from "react";
import { NavigationContainer } from "@react-navigation/native";
import { createNativeStackNavigator } from "@react-navigation/native-stack";
import HomeScreen from "./src/screens/HomeScreen";
import SoulContractScreen from "./src/screens/SoulContractScreen";
import CodexScreen from "./src/screens/CodexScreen";
import { StatusBar } from "expo-status-bar";

const Stack = createNativeStackNavigator();

export default function App() {
  return (
    <NavigationContainer>
      <StatusBar style="auto" />
      <Stack.Navigator initialRouteName="Home" screenOptions={{ headerShown: true }}>
        <Stack.Screen name="Home" component={HomeScreen} />
        <Stack.Screen name="SoulContract" component={SoulContractScreen} options={{ title: "Soul Contract" }} />
        <Stack.Screen name="Codex" component={CodexScreen} options={{ title: "Personal Codex" }} />
      </Stack.Navigator>
    </NavigationContainer>
  );
}
