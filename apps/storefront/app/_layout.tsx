import React from 'react';
import { Stack } from 'expo-router';
import { StatusBar } from 'expo-status-bar';

export default function RootLayout() {
  return (
    <>
      <StatusBar style="light" />
      <Stack
        screenOptions={{
          headerStyle: { backgroundColor: '#080A0F' },
          headerTintColor: '#F1F5F9',
          headerTitleStyle: { fontWeight: 'bold' },
          contentStyle: { backgroundColor: '#080A0F' },
        }}
      >
        <Stack.Screen name="index" options={{ title: 'some-commerce' }} />
      </Stack>
    </>
  );
}
