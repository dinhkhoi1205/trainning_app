import { createNativeStackNavigator } from '@react-navigation/native-stack';
import Activity from './components/Home/Activity';
import { NavigationContainer } from '@react-navigation/native';
import ActivityDetail from './components/Home/ActivityDetail';
import { createBottomTabNavigator } from '@react-navigation/bottom-tabs';
import Login from './components/User/Login';
import Register from './components/User/Register';
import MyUserProfile from './components/User/UserProfile';
import { Icon } from 'react-native-paper';
import { MyDispatchContext, MyUserContext } from './configs/UserContexts';
import { useContext, useReducer } from 'react';
import MyUserReducer from './configs/UserReducer';

const Stack = createNativeStackNavigator();
const Tab = createBottomTabNavigator();

const StackNavigator = () => {
  return (
    <Stack.Navigator screenOptions={{headerShown:false}} >
      <Stack.Screen name='Activity' component={Activity}/>
      <Stack.Screen name='ActivityDetail' component={ActivityDetail}/>
    </Stack.Navigator>
  )
}

const TabNavigator = () => {
const user = useContext(MyUserContext);
  return (
    <Tab.Navigator>
      <Tab.Screen name="home" component={StackNavigator} options={{title: "Main Screen",tabBarIcon: () => <Icon source="home" size={20} />}} />
      {user === null?<>
        <Tab.Screen name="login" component={Login} options={{title: "Log In",tabBarIcon: () => <Icon source="login" size={20} />}}/>
        <Tab.Screen name="register" component={Register} options={{title: "Sign Up", tabBarIcon: () => <Icon source="account-check" size={20} />}}/>
      </>: <>
      <Tab.Screen name="profile" component={MyUserProfile} options={{title: "Account",tabBarIcon: () => <Icon source="account" size={20} />}}/>
      </>}
      
    </Tab.Navigator>
  );
}
export default function App() {
  const [user, dispatch] = useReducer(MyUserReducer, null);

  return (
    <NavigationContainer>
        <MyUserContext.Provider value={user}>
          <MyDispatchContext.Provider value={dispatch}>
            <TabNavigator/>
          </MyDispatchContext.Provider>
        </MyUserContext.Provider>
      </NavigationContainer>
      
  );
}
