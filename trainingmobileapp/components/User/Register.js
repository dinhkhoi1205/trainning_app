import { Button, HelperText, Text, TextInput } from "react-native-paper"
import MyStyles from "../../styles/MyStyles"
import { useState } from "react";
import { Image, KeyboardAvoidingView, Platform, ScrollView, TouchableOpacity, TouchableWithoutFeedback } from "react-native";
import { View } from "react-native";
import * as ImagePicker from 'expo-image-picker';
import { useNavigation } from "@react-navigation/native";

const Register = () => {
    const [user, setUser] = useState({});

    const [loading,setLoading] = useState(false);

    const users = {
        "first_name": {
            "title": "Name",
            "field": "first_name",
            "secure": false,
            "icon": "text"
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

    const [avatar, setAvatar] = useState();
    const nav = useNavigation();
    const [err, setErr] = useState(false);

    const updateUser = (value,field) => {
        setUser({...user, [field]: value});
    }

    const pickImage = async () => {
        let { status } =await ImagePicker.requestMediaLibraryPermissionsAsync();
        if (status !== 'granted') {
            alert("Permissions denied!");
        } else {
        const result =await ImagePicker.launchImageLibraryAsync();
        if (!result.canceled)
            setAvatar(result.assets[0])
        }
    }

    const register = async () => {
        if (user.password !== user.confirm)
                setErr(true);
        else {
            setErr(false);
            let form = new FormData();

            for (let key in user)
                if (key !== 'confirm') {
                    if (key === 'avatar') {
                        form.append('avatar', {
                            uri: user.avatar.uri,
                            name: user.avatar.fileName,
                            type: user.avatar.type
                        })
                    } else
                        form.append(key, user[key]);
                }

            console.info(form)

                
            setLoading(true);
            try {
                let res = await APIs.post(endpoints['register'], form, {
                    headers: {
                        'Content-Type': 'multipart/form-data'
                    }
                });
                console.info(res.data)
                nav.navigate("login");
            } catch (ex) {
                console.error(JSON.stringify(ex));
            } finally {
                setLoading(false);
            }
        }
    }

    return (
    <View style={MyStyles.container}>
        <KeyboardAvoidingView 
        behavior={Platform.OS === 'android' ? 'padding' : 'height'} 
        style={{ flex: 1 }}
        >
                    <HelperText type="error" visible={err}>
                        The password not match
                    </HelperText>

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
                    <TouchableOpacity onPress={pickImage}>
                        <Text style={MyStyles.margin}>Choose profile image</Text>
                    </TouchableOpacity>

                        {avatar ? <Image source={{ uri: avatar.uri }}style={{ width: 100, height: 100 }} /> : ""}

                    <Button onPress={register} loading={loading} icon="account-check" mode="contained">Sign up</Button>

        </KeyboardAvoidingView>
    </View>
    )
    
}

export default Register;