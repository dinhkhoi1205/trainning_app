import { useEffect, useState } from "react";
import APIs, { endpoints } from "../../configs/APIs";
import { ScrollView, Text, Image, View, Alert } from "react-native";
import { ActivityIndicator, Card, List, Button } from "react-native-paper";
import RenderHTML from "react-native-render-html";
import moment from "moment";
import MyStyles from "../../styles/MyStyles";

const ActivityDetail = ({route}) => {
    const activityId = route.params?.activityId;
    const [activity_details, setActivityDetails] = useState(null);
    const [comments, setComments] = useState(null);
    const [isRegistered, setIsRegistered] = useState(false); //Check if registred

    const loadActivityDetails = async () =>{
        let res = await APIs.get(endpoints['activity_details'](activityId));
        setActivityDetails(res.data);
    }

    const loadComments = async () =>{
        let res = await APIs.get(endpoints['comments'](activityId));
        setComments(res.data);
    }

    useEffect(() => {
        loadActivityDetails();
        loadComments();
    }, [activityId]);

    const isCloseToBottom = ({layoutMeasurement, contentOffset, contentSize}) => {
        return layoutMeasurement.height + contentOffset.y >= contentSize.height - 20;
    }

    const reachBottom = ({nativeEvent}) => {
        if (isCloseToBottom(nativeEvent) && comments === null)
            loadComments();
    }

    // Sign up activity
    const handleRegister = async () => {
        try {
            let res = await APIs.post(endpoints['participate-activity'](activityId)); 
            Alert.alert("Success", "You have successful sign up activity");
            setIsRegistered(true); 
        } catch (error) {
            Alert.alert("Error", "Can not sign up activity.");
        }
    };


    return (
        <ScrollView onScroll={reachBottom}>
            {activity_details===null?<ActivityIndicator />:<>
                <Card>
                   
                    <Card.Cover source={{ uri: activity_details.image }} />
                    <Card.Content>
                        <Text variant="titleLarge" style={MyStyles.activity}>{activity_details.title}</Text>
                    
                        <RenderHTML source={{'html': activity_details.description}} />

                        <Text>Start Date: {moment(activity_details.start_date).format("LL")}</Text>
                        <Text>End Date: {moment(activity_details.end_date).format("LL")}</Text>

                        <Text>Max Points: {activity_details.max_point}</Text>

                        <Text>Status: {activity_details.active ? "Active" : "Inactive"}</Text>

                        <Text>Category: {activity_details.category}</Text>

                        {activity_details.tags && activity_details.tags.length > 0 && (
                            <View style={{ marginTop: 10 }}>
                                <Text>Tags:</Text>
                                {activity_details.tags.map((tag, index) => (
                                    <Text key={index}>{tag.name}</Text>
                                ))}
                            </View>
                        )}

                            <Button
                                mode="contained"
                                onPress={handleRegister}
                                disabled={isRegistered}
                                style={{ marginTop: 10 }}
                            >
                                {isRegistered ? "Have sign up already" : "Join event"}
                            </Button>
                    </Card.Content>
                    
                    
                </Card>
            </>}

            <View>
            <View>
                {comments === null ? <ActivityIndicator /> : <>
                    {comments.map(c => (
                        <List.Item
                            key = {c.id || index}
                            title={c.content}
                            description={moment(c.created_date).fromNow()}  
                            left={() => <Image style={MyStyles.box} source={{ uri: c.user.avatar }} />} 
                        />
                    ))}
                </>}
            </View>
            </View>
        </ScrollView>
    );
}

export default ActivityDetail;
