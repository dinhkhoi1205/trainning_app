import { View, Text } from "react-native"
import MyStyles from "../../styles/MyStyles"
import { useState } from "react"

const Home = () => {
    const [categories, setCategories] = useState([]);

    const loadCates = async () => {
        let res = await APIs.get
    }
    return (
        <View style={MyStyles.container}>
            <Text style={MyStyles.activity}>ACTIVITIES LIST</Text>
        </View>
    )
}

export default Home;