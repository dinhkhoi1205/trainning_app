import { createNativeStackNavigator } from '@react-navigation/native-stack';
import Home from './components/Home/Home'
import Activities from './components/Home/Activities';
import { NavigationContainer } from '@react-navigation/native';

const Stack = createNativeStackNavigator()

const StackNavigator = () => {
  return (
    <Stack.Navigator>
      <Stack.Screen name='index' component={Home}/>
      <Stack.Screen name='activities' component={Activities}/>
    </Stack.Navigator>
  )
}
export default function App() {
  return (
    <NavigationContainer>
      <StackNavigator/>
    </NavigationContainer>
  );
}
