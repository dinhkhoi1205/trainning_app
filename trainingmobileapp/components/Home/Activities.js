import { Text } from "react-native"
import MyStyles from "../../styles/MyStyles"

const Activities = ({ route }) => {
    const activityId = route.params?.activityId
    return (
        <Text style={MyStyles.activity}>Activity Information {activityId}</Text>
    );
}

export default Activities;