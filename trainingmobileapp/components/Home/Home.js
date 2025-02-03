import { View, Text, Image, TouchableOpacity, FlatList } from "react-native";
import MyStyles from "../../styles/MyStyles";
import { useEffect, useState } from "react";
import APIs, { endpoints } from "../../configs/APIs";
import { ActivityIndicator, Chip, List } from "react-native-paper";

const Home = () => {
    const [categories, setCategories] = useState([]);
    const [activities, setActivities] = useState([]);
    const [loading, setLoading] = useState(false);
    const [cateId, setCateId] = useState(null);
    const [page, setPage] = useState(1);

    const loadCates = async () => {
        let res = await APIs.get(endpoints['categories']);
        setCategories(res.data);
    };

    const loadActivities = async () => {
        if (page > 0) {
            setLoading(true);
            try {
                let url = `${endpoints['activities']}?page=${page}`;
                if (cateId)
                    url += `&category_id=${cateId}`;

                let res = await APIs.get(url);
                setActivities(page === 1 ? res.data.results : [...activities, ...res.data.results]);

                if (res.data.next === null)
                    setPage(0);
            } catch (ex) {
                console.error(ex);
            } finally {
                setLoading(false);
            }
        }
    };

    useEffect(() => {
        loadCates();
    }, []);

    useEffect(() => {
        setActivities([]); 
        setPage(1); 
        loadActivities();
    }, [cateId]);

    useEffect(() => {
        loadActivities();
    }, [page]);

    const loadMore = () => {
        if (page > 0 | loading) setPage(page + 1);
    };

    return (
        <View style={MyStyles.container}>
            <Text style={MyStyles.activity}>ACTIVITIES LIST</Text>

            <View style={MyStyles.row}>
                {categories.map(c => (
                    <TouchableOpacity onPress={() => setCateId(c.id)} key={c.id}>
                        <Chip style={MyStyles.margin} icon="label">{c.name}</Chip>
                    </TouchableOpacity>
                ))}
            </View>

            {loading && <ActivityIndicator />}

            <FlatList 
                data={activities} 
                onEndReached={loadMore}
                keyExtractor={(item) => item.id.toString()}
                renderItem={({ item }) => (
                    <List.Item 
                        title={item.title} 
                        description={item.start_date}  
                        left={props => (
                            <Image style={MyStyles.box} source={{ uri: item.image }} />
                        )}
                    />
                )}
            />
        </View>
    );
}

export default Home;
