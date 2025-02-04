import { createNativeStackNavigator } from '@react-navigation/native-stack';
import Activity from './components/Home/Activity';
import { NavigationContainer } from '@react-navigation/native';
import ActivityDetail from './components/Home/ActivityDetail';

const Stack = createNativeStackNavigator()

const StackNavigator = () => {
  return (
    <Stack.Navigator>
      <Stack.Screen name='Activity' component={Activity}/>
      <Stack.Screen name='ActivityDetail' component={ActivityDetail}/>
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
