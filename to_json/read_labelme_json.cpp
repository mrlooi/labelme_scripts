#include <iostream>
#include <vector>
#include <fstream>
#include <json.hpp>

#include <opencv2/opencv.hpp>

bool read_labelme_json(const std::string json_file, std::vector<cv::Rect>& bboxes, std::vector<std::vector<cv::Point>>& contours)
{
    std::ifstream f(json_file);
    if (!f.good())
    {
        printf("Could not find file %s\n!", json_file.c_str());
        return false;
    }
    nlohmann::json j;

    bool succ = false;
    try 
    {
        f >> j;
        
        for (int k = 0; k < j.size(); ++k)
        {
            auto& jk = j[k];
            std::string cls = jk["type"];
            float score = jk["score"];
            const std::vector<int>& bbox = jk["bbox"]; // x1 y1 x2 y2
            
            const std::vector<int>& flattened_contours = jk["contours"]; // x y x y ...
            std::vector<cv::Point> contour_points(flattened_contours.size()/2);

            for (int i = 0; i < contour_points.size(); ++i)
            {
                contour_points[i] = cv::Point(flattened_contours[i*2],flattened_contours[i*2+1]);
            }

            bboxes.push_back({bbox[0], bbox[1], bbox[2]-bbox[0], bbox[3]-bbox[1]});
            contours.push_back(contour_points);
        }

        succ = true;
    } 
    catch (const std::invalid_argument& ia)
    {
        std::cerr << "INVALID JSON in " << json_file << std::endl;
    }
    f.close();

    return succ;
}

int main(int argc, char *argv[])
{
    std::string json_file = "../../box/data_0_1506658963436.json";
    // std::string img_file = "../../box/data_0_1506658963436.jpg";
    std::vector<cv::Rect> bboxes; 
    std::vector<std::vector<cv::Point>> contours;

    read_labelme_json(json_file, bboxes, contours);

    printf("Contours size: %d\n", contours.size());

    return 0;
}

