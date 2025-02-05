import { useCallback, useEffect, useRef, useState } from "react";
import APIs, { authApis, endpoints } from "../../configs/APIs";
import { ScrollView, Text, Image, View, Alert } from "react-native";
import { ActivityIndicator, Card, List, Button } from "react-native-paper";
import RenderHTML from "react-native-render-html";
import moment from "moment";
import MyStyles from "../../styles/MyStyles";
import { useFocusEffect } from "@react-navigation/native";

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

   

    const isCloseToBottom = ({layoutMeasurement, contentOffset, contentSize}) => {
        return layoutMeasurement.height + contentOffset.y >= contentSize.height - 20;
    }

    const reachBottom = ({nativeEvent}) => {
        if (isCloseToBottom(nativeEvent) && comments === null)
            loadComments();
    }

    const checkRegistrationStatus = async () => {
        try {
            const api = await authApis();
    
            // Lấy thông tin user hiện tại
            const userResponse = await api.get(endpoints.current_user);
            if (!userResponse.data || !userResponse.data.id) {
                console.error("Lỗi: Không lấy được ID user!");
                return;
            }
    
            const userId = userResponse.data.id;
            console.log("User ID:", userId); // Debug user ID
    
            // Kiểm tra danh sách đăng ký
            const response = await api.get(endpoints.activity_register(activityId));
            console.log("Danh sách người đăng ký:", response.data); // Debug danh sách đăng ký
    
            if (response.data && response.data.length > 0) {
                // Kiểm tra xem user hiện tại có trong danh sách không
                const isUserRegistered = response.data.some(reg => reg.user && reg.user.id === userId);
                console.log("Trạng thái đăng ký:", isUserRegistered); // Debug trạng thái đăng ký
                setIsRegistered(isUserRegistered);
            } else {
                setIsRegistered(false);
            }
        } catch (error) {
            console.error("Lỗi khi kiểm tra trạng thái đăng ký:", error);
        }
    }

    const handleRegisterActivity = async () => {
        try {
            // Check status if register activity
            if (isRegistered) {
                Alert.alert("Alert", "You have joined already");
                return; 
            }
    
            const api = await authApis();
            const response = await api.post(endpoints.activity_register(activityId));
    
            if (response.status === 201) {
                Alert.alert("Success", "You have signed successfully!");
                setIsRegistered(true); // Update status
            } else {
                Alert.alert("Error", "Have error");
            }
        } catch (error) {
            console.error("Error when sign activity", error);
            Alert.alert("Error", "Can not join activity");
        }
    };

    useEffect(() => {
        loadActivityDetails();
        loadComments();
    }, [activityId]);

    useEffect(() => {
        checkRegistrationStatus(); //Check status again
    }, [isRegistered]); // Every status change
    

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
                                onPress={handleRegisterActivity}
                                disabled={isRegistered}
                                style={{ marginTop: 10 }}
                            >
                            </Button>
                    </Card.Content>
                    
                    
                </Card>
            </>}

            <View>
            <View>
                {comments === null ? <ActivityIndicator /> : <>
                    {comments.map(c => (
                        <List.Item
                            key={c.id ? `comment-${c.id}` : `comment-${index}`} 
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
