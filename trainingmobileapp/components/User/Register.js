import { Button, HelperText, Text, TextInput } from "react-native-paper"
import MyStyles from "../../styles/MyStyles"
import { useState } from "react";
import { Image, KeyboardAvoidingView, Platform, ScrollView, TouchableOpacity, TouchableWithoutFeedback } from "react-native";
import { View } from "react-native";
import * as ImagePicker from 'expo-image-picker';
import { useNavigation } from "@react-navigation/native";
import APIs,{endpoints} from "../../configs/APIs";

const Register = () => {
    const [user, setUser] = useState({
        "username": "",
        "password": ""
    });
    const [loading,setLoading] = useState(false);
    const [avatar, setAvatar] = useState();
    const nav = useNavigation();
    const updateUser = (value,field) => {
        setUser({...user, [field]: value});
    }
    const users = {
        "first_name": {
            "title": "First Name",
            "field": "first_name",
            "secure": false,
            "icon": "text"
        },
        "last_name": {
            "title": "Last Name",
            "field": "last_name",
            "icon": "text",
            "secure": false
        },
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
        }, "confirm": {
            "title": "Confirm Password",
            "field": "confirm",
            "secure": true,
            "icon": "eye"
        }
    }

    const pickImage = async () => {
        let { status } =await ImagePicker.requestMediaLibraryPermissionsAsync();
        if (status !== 'granted') {
            alert("Permissions denied!");
        } else {
        const result =await ImagePicker.launchImageLibraryAsync();
        if (!result.canceled)
            setAvatar(result.assets[0]);
        }
    }

    const register = async () => {
        
        setLoading(true);
        try {
            const form = new FormData();

            for (let k in user)
                if (k !== 'confirm')
                    form.append(k, user[k]);

            console.info(form);

            form.append('avatar', {
                uri: avatar.uri,
                name: avatar.fileName || avatar.uri.split('/').pop(),
                type: avatar.type || 'image/jpeg'
            });

            
            await APIs.post(endpoints['register'], form, {
                headers: {
                    'Content-Type': 'multipart/form-data'
                }
            });

            nav.navigate("login");
        } catch (ex) {
            console.error("Registration error:", ex);
        } finally {
            setLoading(false);
        }
    }
    return (
    <View style={MyStyles.container}>
        <KeyboardAvoidingView 
        behavior={Platform.OS === 'android' ? 'padding' : 'height'} 
        style={{ flex: 1 }}
        >
                    {Object.values(users).map(u => (
                        <TextInput 
                            key={u.field} 
                            right={<TextInput.Icon icon={u.icon} />}
                            placeholder={u.title} 
                            style={MyStyles.margin} 
                            secureTextEntry={u.secure}
                            value={user[u.field] || ""} 
                            onChangeText={t => updateUser(t, u.field)}
                        />
                    ))}
                    <TouchableOpacity onPress={pickImage}>
                        <Text style={MyStyles.margin}>Choose profile image</Text>
                    </TouchableOpacity>

                    {avatar ? <Image source={{ uri: avatar.uri }} style={{ width: 100, height: 100 }} /> : ""}

                    <Button onPress={register} loading={loading} icon="account-check" mode="contained">Sign up</Button>

        </KeyboardAvoidingView>
    </View>
    )
    
}

export default Register;