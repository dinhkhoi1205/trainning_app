import { Button, Text } from "react-native-paper"
import MyStyles from "../../styles/MyStyles"
import { useContext } from "react"
import { MyDispatchContext, MyUserContext } from "../../configs/UserContexts"
import AsyncStorage from "@react-native-async-storage/async-storage"

const MyUserProfile = () => {
    const user = useContext(MyUserContext)
    const dispatch = useContext(MyDispatchContext)

    const logout = async () => {
        await AsyncStorage.removeItem("token");
        dispatch({
            "type" : "logout"
        });
      
    }
    return (
        <>
            <>
                <Text style={MyStyles.activity}>Hello {user?.username}</Text>
                <Button onPress={logout} style={MyStyles.margin} mode="contained-tonal">
                    Log out
                </Button>
            </>
    
         </>

    )
}

export default MyUserProfile;