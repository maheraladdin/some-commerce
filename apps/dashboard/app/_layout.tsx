import React from 'react';
import { Stack } from 'expo-router';
import { StatusBar } from 'expo-status-bar';

export default function DashboardLayout() {
  return (
    <>
      <StatusBar style="light" />
      <Stack
        screenOptions={{
          headerShown: false,
          contentStyle: { backgroundColor: '#080A0F' },
        }}
      >
        <Stack.Screen name="index" options={{ title: 'Dashboard Overview' }} />
        <Stack.Screen name="admin/sdui-studio" options={{ title: 'SDUI Studio' }} />
        <Stack.Screen name="vendor/dashboard" options={{ title: 'Vendor Portal' }} />
      </Stack>
    </>
  );
}
