import { useEffect, useState } from "react";
import APIs, { endpoints } from "../../configs/APIs";
import { ScrollView, Text, Image, View } from "react-native";
import { ActivityIndicator, Card, List } from "react-native-paper";
import RenderHTML from "react-native-render-html";
import moment from "moment";

const ActivityDetail = ({route}) => {
    const activityId = route.params?.activityId;
    const [activityDetails, setActivityDetails] = useState(null);
    const [comments, setComments] = useState(null);

    const loadActivityDetails = async () =>{
        let res = await APIs.get(endpoints['activity-details'](activityId));
        setActivityDetails(res.data);
    }

    const loadComments = async () =>{
        let res = await APIs.get(endpoints['comments'](activityId));
        setComments(res.data);
    }

    useEffect(() => {
        loadActivityDetails();
    }, [activityId]);

    const isCloseToBottom = ({layoutMeasurement, contentOffset, contentSize}) => {
        return layoutMeasurement.height + contentOffset.y >= contentSize.height - 20;
    }

    const reachBottom = ({nativeEvent}) => {
        if (isCloseToBottom(nativeEvent) && comments === null)
            loadComments();
    }

    return (
        <ScrollView onScroll={reachBottom}>
            {activityDetails===null?<ActivityIndicator />:<>
                <Card>
                   
                    <Card.Cover source={{ uri: activityDetails.image }} />
                    <Card.Content>
                        <Text variant="titleLarge" style={MyStyles.activity}>{activityDetails.title}</Text>
                    
                        <RenderHTML source={{'html': activityDetails.description}} />

                        <Text>Start Date: {moment(activityDetails.start_date).format("LL")}</Text>
                        <Text>End Date: {moment(activityDetails.end_date).format("LL")}</Text>

                        <Text>Max Points: {activityDetails.max_point}</Text>

                        <Text>Status: {activityDetails.active ? "Active" : "Inactive"}</Text>

                        <Text>Category: {activityDetails.category}</Text>

                        {activityDetails.tags && activityDetails.tags.length > 0 && (
                            <View style={{ marginTop: 10 }}>
                                <Text>Tags:</Text>
                                {activityDetails.tags.map((tag, index) => (
                                    <Text key={index}>{tag.name}</Text>
                                ))}
                            </View>
                        )}
                    </Card.Content>
                    
                    
                </Card>
            </>}

            <View>
            <View>
                {comments === null ? <ActivityIndicator /> : <>
                    {comments.map(c => (
                        <List.Item
                            title={c.content}
                            description={moment(c.created_date).fromNow()}  
                            left={() => <Image style={MyStyles.box} source={{ uri: c.user.image }} />} 
                        />
                    ))}
                </>}
            </View>
            </View>
        </ScrollView>
    );
}

export default ActivityDetail;
