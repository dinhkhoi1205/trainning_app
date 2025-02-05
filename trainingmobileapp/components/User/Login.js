import { Button, Text, TextInput } from "react-native-paper"
import MyStyles from "../../styles/MyStyles"
import { useContext, useEffect, useState } from "react"
import APIs, { authApis, endpoints } from "../../configs/APIs";
import { Keyboard, KeyboardAvoidingView, Platform, View } from "react-native";
import AsyncStorage from "@react-native-async-storage/async-storage";
import { MyDispatchContext } from "../../configs/UserContexts";
import { useNavigation } from "@react-navigation/native";

const Login = () => {
    const [user, setUser] = useState({});

    const [loading,setLoading] = useState(false);
    const dispatch = useContext(MyDispatchContext);
    const nav = useNavigation();

    const users = {
        "username" : {
            "title" : "Username",
            "field" : "username",
            "secure" : false,
            "icon" : "text"
        },
            "password" : {
                "title" : "Password",
                "field" : "password",
                "secure" : true,
                "icon" : "eye"
        }
    }

   

    const updateUser = (value,field) => {
        setUser({...user, [field]: value});
    }

    const login = async () => {
        setLoading(true);
       try{
   
        let res = await APIs.post(endpoints['login'], {
            
            'client_id' : 'gsJrvOcfSnnywuz9PCJVWQf4cHWJuaFQcjE6TLpD',
            'client_secret' : '0RJXyvvTJ6MjhVmG9IgSJlwGUjCIlQKkkzqOTdN61AfUBqZ5nw9tLT1g4leWULUpU5jDdgr6nu7HRh826Afm6quGieSNvRTgzRBT5I3tnOLWt2c2xsxb0oajLDA21Itn',
            'grant_type' : 'password',
            ...user
        });
        console.info(res.data.access_token);
        await AsyncStorage.setItem('token', res.data.access_token);

        setTimeout(async () => {
            let user = await authApis(res.data.access_token).get(endpoints['current_user']);
            console.info(user.data);

            dispatch({
                "type": "login",
                "payload": user.data
            });

            console.info("Đã cập nhật UserContext!");

            nav.navigate("home");

        }, 100);

       } catch (ex){
        console.error("Login failed", ex);
       } finally{
        setLoading(false);
       }
    }

    return (
        <KeyboardAvoidingView 
            behavior={Platform.OS === 'ios' ? 'padding' : 'height'} 
            style={{ flex: 1 }}
        >
                    <View>
                        {Object.values(users).map(u => (
                            <TextInput 
                                key={u.field} 
                                right={<TextInput.Icon icon={u.icon} />}
                                placeholder={u.title} 
                                style={MyStyles.margin} 
                                secureTextEntry={u.secure}
                                value={user[u.field]} 
                                onChangeText={t => updateUser(t, u.field)}
                            />
                        ))}
                        
                        <Button onPress={login} loading={loading} icon="account-check" mode="contained">Log in</Button>
                    </View>
        </KeyboardAvoidingView>
    );
};
export default Login;