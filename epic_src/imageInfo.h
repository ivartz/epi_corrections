#ifndef GUARD_imageInfo
#define GUARD_imageInfo

struct IMAGEINFO {
  int   firstImageDirection; //  -1 or 1, where +1 = forward, -1 = reverse.
  int   numVox[3];
  float voxSize[3];          // This will be useful later, but currently we're not using it.
  int   numFrames;           // Ignored or set to 2 for the above routine, used in next routine.
};

#endif
