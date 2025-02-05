import { useCallback, useEffect, useRef, useState } from "react";
import APIs, { authApis, endpoints } from "../../configs/APIs";
import { ScrollView, Text, Image, View, Alert } from "react-native";
import { ActivityIndicator, Card, List, Button, TextInput } from "react-native-paper";
import RenderHTML from "react-native-render-html";
import moment from "moment";
import MyStyles from "../../styles/MyStyles";


const ActivityDetail = ({route}) => {
    const activityId = route.params?.activityId;
    const [activity_details, setActivityDetails] = useState(null);
    const [comments, setComments] = useState(null);
    const [isRegistered, setIsRegistered] = useState(false); //Check if registred
    const [newComment, setNewComment] = useState('');

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
    
            // Take user ID
            const userResponse = await api.get(endpoints.current_user);
            if (!userResponse.data || !userResponse.data.id) {
                console.error("Error: Cannot take user ID!");
                return;
            }
    
            const userId = userResponse.data.id;
            console.log("User ID:", userId); // Debug user ID
    
            // Check register list activity
            const response = await api.get(endpoints['activity_register'](activityId));
            console.log("Activity register list", response.data); 
    
            if (response.data && response.data.length > 0) {
                // Check if user in register activity
                const isUserRegistered = response.data.some(reg => reg.user && reg.user.id === userId);
                console.log("Status", isUserRegistered); 
                setIsRegistered(isUserRegistered);
            } else {
                setIsRegistered(false);
            }
        } catch (error) {
            console.error("Error when check status:", error);
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
            const response = await api.post(endpoints['activity_register'](activityId));
    
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


    const handleSubmitComment = async () => {
        if (!newComment.trim()) {
            Alert.alert("Error", "Please enter a comment.");
            return;
        }
    
        try {
            const api = await authApis();
            const response = await api.post(endpoints['post_comment'](activityId), {
                content: newComment.trim(),
            });
    
            if (response.status === 201) {
                Alert.alert("Success", "Your comment has been posted.");
                setNewComment('');  // Clear input after successful post
    
                // Cập nhật comments trực tiếp thay vì gọi loadComments()
                const newCommentData = {
                    id: response.data.id,  // Giả sử server trả về ID của comment
                    content: newComment.trim(),
                    created_date: moment().toISOString(),
                    user: { avatar: 'URL_OF_AVATAR' } // Dữ liệu người dùng, có thể lấy từ server
                };
                setComments(prevComments => [newCommentData, ...prevComments]);  // Thêm comment mới vào đầu danh sách
            } else {
                Alert.alert("Error", "There was an issue posting your comment.");
            }
        } catch (error) {
            console.error("Error posting comment", error);
            Alert.alert("Error", "There was an error submitting your comment.");
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

                        {activity_details.categories && activity_details.categories.length > 0 && (
                            <View style={{ marginTop: 10 }}>
                                <Text>Category:</Text>
                                {activity_details.categories.map((category, index) => (
                                    <Text key={index}>{category.name}</Text>
                                ))}
                            </View>
                        )}

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
                                Join activity
                            </Button>

                    </Card.Content>
                    
                </Card>
            </>}

            <View>
            <View style={{ marginTop: 20 }}>
                <TextInput
                    label="Write a comment"
                    value={newComment}
                    onChangeText={setNewComment}
                    mode="outlined"
                    multiline
                    numberOfLines={3}
                    style={{ marginBottom: 10 }}
                />
                <Button
                    mode="contained"
                    onPress={handleSubmitComment}
                    disabled={!newComment.trim()}
                >
                    Post Comment
                </Button>
            </View>
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
