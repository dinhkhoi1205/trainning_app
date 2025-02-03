import { View, Text } from "react-native"
import MyStyles from "../../styles/MyStyles"
import { useEffect, useState } from "react"
import APIs,{ endpoints } from "../../configs/APIs";
import { Chip } from "react-native-paper";

const Home = () => {
    const [categories, setCategories] = useState([]);

    const loadCates = async () => {
        let res = await APIs.get(endpoints['categories']);
        console.info(res.data);
        setCategories(res.data);
    }

    useEffect(() => {
        loadCates();

    }, [])
    return (
        <View style={MyStyles.container}>
            <Text style={MyStyles.activity}>ACTIVITIES LIST</Text>
            <View style={MyStyles.row}>
            {categories.map(c => <Chip style={MyStyles.margin} icon="label" key={c.id}>{c.name}</Chip>)}
            </View>
        </View>
    )
}

export default Home;