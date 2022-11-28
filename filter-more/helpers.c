#include "helpers.h"
#include <math.h>
#include <stdio.h>
#include <string.h>
#include <stdlib.h>

// Convert image to grayscale
void grayscale(int height, int width, RGBTRIPLE image[height][width])
{
    float avg;

    // Loop through all pixels
    for (int i = 0; i < height; i++)
    {
        for (int j = 0; j < width; j++)
        {
            avg = (image[i][j].rgbtBlue + image[i][j].rgbtGreen + image[i][j].rgbtRed) / 3.0;
            image[i][j].rgbtBlue = round(avg);
            image[i][j].rgbtGreen = round(avg);
            image[i][j].rgbtRed = round(avg);
        }
    }
    return;
}

// Reflect image horizontally
void reflect(int height, int width, RGBTRIPLE image[height][width])
{
    // Loop through all pixels
    for (int i = 0; i < height; i++)
    {
        // Inverting row
        for (int j = 0; j < width / 2; j++)
        {
            RGBTRIPLE tmp = image[i][j];

            image[i][j].rgbtBlue = image[i][width - 1 - j].rgbtBlue;
            image[i][j].rgbtGreen = image[i][width - 1 - j].rgbtGreen;
            image[i][j].rgbtRed = image[i][width - 1 - j].rgbtRed;

            image[i][width - 1 - j].rgbtBlue = tmp.rgbtBlue;
            image[i][width - 1 - j].rgbtGreen = tmp.rgbtGreen;
            image[i][width - 1 - j].rgbtRed = tmp.rgbtRed;
        }
    }
    return;
}

// Blur image
void blur(int height, int width, RGBTRIPLE image[height][width])
{
    // Temporary array for not messing up pixel values
    RGBTRIPLE tmp[height][width];
    memcpy(tmp, image, height * width * sizeof(RGBTRIPLE));

    // Loop through all pixels
    for (int i = 0; i < height; i++)
    {
        for (int j = 0; j < width; j++)
        {
            float total_b = 0;
            float total_g = 0;
            float total_r = 0;
            float counter = 0;

            // Loop through 3x3 grid
            for (int k = -1; k <= 1; k++)
            {
                for (int k2 = -1; k2 <= 1; k2++)
                {
                    // If grid position exists
                    if ((i + k) >= 0 && (i + k) < height && (j + k2) >= 0 && (j + k2) < width)
                    {
                        total_b += (float) tmp[i + k][j + k2].rgbtBlue;
                        total_g += (float) tmp[i + k][j + k2].rgbtGreen;
                        total_r += (float) tmp[i + k][j + k2].rgbtRed;
                        counter++;
                    }
                }
            }
            // Assign results to original array
            image[i][j].rgbtBlue = round(total_b / counter);
            image[i][j].rgbtGreen = round(total_g / counter);
            image[i][j].rgbtRed = round(total_r / counter);
        }
    }
    return;
}

// Detect edges
void edges(int height, int width, RGBTRIPLE image[height][width])
{
    // Temporary array for not messing up pixel values
    RGBTRIPLE tmp[height][width];
    memcpy(tmp, image, height * width * sizeof(RGBTRIPLE));

    int gx_weights[] = {-1, 0, 1, -2, 0, 2, -1, 0, 1};
    int gy_weights[] = {-1, -2, -1, 0, 0, 0, 1, 2, 1};


    // Loop through all pixels
    for (int i = 0; i < height; i++)
    {
        for (int j = 0; j < width; j++)
        {
            float gx_b = 0;
            float gy_b = 0;
            float gx_g = 0;
            float gy_g = 0;
            float gx_r = 0;
            float gy_r = 0;
            int counter = 0;

            // Loop through 3x3 grid
            for (int k = -1; k <= 1; k++)
            {
                for (int k2 = -1; k2 <= 1; k2++)
                {
                    // If pixel is not on border
                    if ((i + k) >= 0 && (i + k) < height && (j + k2) >= 0 && (j + k2) < width)
                    {
                        gx_b += (float) gx_weights[counter] * tmp[i + k][j + k2].rgbtBlue;
                        gy_b += (float) gy_weights[counter] * tmp[i + k][j + k2].rgbtBlue;
                        gx_g += (float) gx_weights[counter] * tmp[i + k][j + k2].rgbtGreen;
                        gy_g += (float) gy_weights[counter] * tmp[i + k][j + k2].rgbtGreen;
                        gx_r += (float) gx_weights[counter] * tmp[i + k][j + k2].rgbtRed;
                        gy_r += (float) gy_weights[counter] * tmp[i + k][j + k2].rgbtRed;
                    }
                    counter++;
                }
            }

            // Assign results
            if (sqrt(pow(gx_b, 2) + pow(gy_b, 2)) > 255)
            {
                image[i][j].rgbtBlue = 255;
            }
            else
            {
                image[i][j].rgbtBlue = round(sqrt(pow(gx_b, 2) + pow(gy_b, 2)));
            }
            if (sqrt(pow(gx_g, 2) + pow(gy_g, 2)) > 255)
            {
                image[i][j].rgbtGreen = 255;
            }
            else
            {
                image[i][j].rgbtGreen = round(sqrt(pow(gx_g, 2) + pow(gy_g, 2)));
            }
            if (sqrt(pow(gx_r, 2) + pow(gy_r, 2)) > 255)
            {
                image[i][j].rgbtRed = 255;
            }
            else
            {
                image[i][j].rgbtRed = round(sqrt(pow(gx_r, 2) + pow(gy_r, 2)));
            }
        }
    }
    return;
}
