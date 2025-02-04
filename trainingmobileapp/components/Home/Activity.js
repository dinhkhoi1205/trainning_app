import { View, Text, Image, TouchableOpacity, FlatList, RefreshControl } from "react-native";
import MyStyles from "../../styles/MyStyles";
import { useEffect, useState } from "react";
import APIs, { endpoints } from "../../configs/APIs";
import { ActivityIndicator, Chip, List, Searchbar } from "react-native-paper";
import { useNavigation } from "@react-navigation/native";

const Activity = () => {
    const [categories, setCategories] = useState([]);
    const [activities, setActivities] = useState([]);
    const [loading, setLoading] = useState(false);
    const [cateId, setCateId] = useState(null);
    const [page, setPage] = useState(1);
    const [q, setQ] = useState("");
    const nav = useNavigation();

    // Load categories list
    const loadCates = async () => {
        let res = await APIs.get(endpoints['categories']);
        setCategories(res.data);
    };

    // Load activities list
    const loadActivities = async () => {
        if (page > 0) {
            setLoading(true);
            try {
                let url = `${endpoints['activities']}?page=${page}`;
                let params = [];

                if (cateId !== null) params.push(`category_id=${cateId}`);
                if (q) params.push(`q=${q}`);
                
                if (params.length > 0) url += `&${params.join("&")}`;


                let res = await APIs.get(url);

                if (page === 1) {
                    setActivities(res.data.results); // Reset list when new filter
                } else {
                    setActivities(prev => [...prev, ...res.data.results]);
                }

                if (res.data.next === null) setPage(0);
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
        let timer = setTimeout(() => loadActivities(), 500);
        return () => clearTimeout(timer);
    }, [cateId, page, q]);

    // When pick categories, reset list
    const handleCategorySelect = (id) => {
        setCateId(id);
        setPage(1);
        setActivities([]); // Reset list to new list
    };

    // When press "All activities"
    const showAllActivities = () => {
        setCateId(null); // Reset cateId to take all activities
        setPage(1);
        setActivities([]);
    };

    // When search, reset new list
    const handleSearch = (text) => {
        setQ(text);
        setPage(1);
        setActivities([]);
    };

    // When clear search, reset list
    const clearSearch = () => {
        setQ("");
        setPage(1);
        setActivities([]);
        loadActivities();
    };

    // Load more page when scrolling down
    const loadMore = () => {
        if (page > 0 && !loading) setPage(prev => prev + 1);
    };
    
    //Refresh page
    const refresh = () => {
        setPage(1);
        loadActivities([]);
    }

    return (
        <View style={MyStyles.container}>
            <Text style={MyStyles.activity}>ACTIVITIES LIST</Text>

            {/* Activities list */}
            <View style={MyStyles.row}>

                     {/* Button "All activities" */}
                <TouchableOpacity onPress={showAllActivities}>
                    <Chip style={MyStyles.margin} icon="label" selected={cateId === null}>
                        All activities
                    </Chip>
                </TouchableOpacity>
                
                {/* Button with different categories */}
                {categories.map(c => (
                    <TouchableOpacity onPress={() => handleCategorySelect(c.id)} key={c.id}>
                        <Chip style={MyStyles.margin} icon="label" selected={cateId === c.id}>
                            {c.name}
                        </Chip>
                    </TouchableOpacity>
                ))}

            </View>

            {loading && <ActivityIndicator />}

            {/* Search bar */}
            <Searchbar
                placeholder="Search for activities"
                value={q}
                onChangeText={handleSearch}
                onClearIconPress={clearSearch}
            />

            {/* Activities list */}
            <FlatList 
                data={activities} 
                onEndReached={loadMore}
                keyExtractor={(item) => item.id.toString()}
                renderItem={({ item }) => (
                    <List.Item 
                        title={item.title} 
                        description={item.start_date}  
                        left={props => (
                            <TouchableOpacity onPress={() => nav.navigate('ActivityDetail', {activityId: item.id})}>
                                <Image style={MyStyles.box} source={{ uri: item.image }} />
                            </TouchableOpacity>
                        )}
                    />
                )}
                refreshControl={
                    <RefreshControl refreshing={loading} onRefresh={refresh} />
                }
            />
        </View>
    );
}

export default Activity;
