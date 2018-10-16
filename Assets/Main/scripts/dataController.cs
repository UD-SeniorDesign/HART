using System.Collections;
using System.Collections.Generic;
using System.IO;
using UnityEngine;

public class dataController : MonoBehaviour
{
    private string gameDataFileName = "gps_data.json";
    private List<gpsData> GPSData;
    // Use this for initialization
    void Start()
    {
        GPSData = new List<gpsData>();
        ReadFile();
    }
    void ReadFile()
    {
        string filePath = Path.Combine(Application.streamingAssetsPath, gameDataFileName);
        if (File.Exists(filePath))
        {
            char[] toTrim = { '[', ',',']'};
            foreach (string json in File.ReadAllLines(filePath))
            {
                string tmp  = json.Trim(toTrim);
                //Debug.Log(tmp);
                GPSData.Add(JsonUtility.FromJson<gpsData>(tmp));
                //Debug.Log(GPSData[GPSData.Count - 1].Elevation);
            }
        }
        else
        {
            Debug.LogError("Cannot load game data!");
        }
    }
    public gpsData getGPS(int idx)
    {
        return GPSData[idx % GPSData.Count];
    }
}
