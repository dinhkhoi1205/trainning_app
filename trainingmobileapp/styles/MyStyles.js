import { StyleSheet } from "react-native";

export default StyleSheet.create({
    container: {
        flex: 1,
        padding: 5,
        // justifyContent: "center",
        // alignItems: "center"
    }, row: {
        flexDirection: "row",
        flexWrap: "wrap"
    },
     activity: {
        fontSize: 20,
        fontWeight: "bold",
        color: "blue",
        textAlign: "center", 
        marginTop: 30,        
        alignSelf: "center", 
    }, margin: {
        margin: 5
    }, box: {
        width: 80,
        height: 80,
        borderRadius: 10
    }
});

