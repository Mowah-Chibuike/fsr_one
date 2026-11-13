#ifndef FSR_CONTROLLERS__VISIBILITY_CONTROL_H_
#define FSR_CONTROLLERS__VISIBILITY_CONTROL_H_

// This logic was borrowed (then namespaced) from the examples on the gcc wiki:
//     https://gcc.gnu.org/wiki/Visibility

#if defined _WIN32 || defined __CYGWIN__
#ifdef __GNUC__
#define FSR_CONTROLLERS_EXPORT __attribute__((dllexport))
#define FSR_CONTROLLERS_IMPORT __attribute__((dllimport))
#else
#define FSR_CONTROLLERS_EXPORT __declspec(dllexport)
#define FSR_CONTROLLERS_IMPORT __declspec(dllimport)
#endif
#ifdef FSR_CONTROLLERS_BUILDING_DLL
#define FSR_CONTROLLERS_PUBLIC FSR_CONTROLLERS_EXPORT
#else
#define FSR_CONTROLLERS_PUBLIC FSR_CONTROLLERS_IMPORT
#endif
#define FSR_CONTROLLERS_PUBLIC_TYPE FSR_CONTROLLERS_PUBLIC
#define FSR_CONTROLLERS_LOCAL
#else
#define FSR_CONTROLLERS_EXPORT __attribute__((visibility("default")))
#define FSR_CONTROLLERS_IMPORT
#if __GNUC__ >= 4
#define FSR_CONTROLLERS_PUBLIC __attribute__((visibility("default")))
#define FSR_CONTROLLERS_LOCAL __attribute__((visibility("hidden")))
#else
#define FSR_CONTROLLERS_PUBLIC
#define FSR_CONTROLLERS_LOCAL
#endif
#define FSR_CONTROLLERS_PUBLIC_TYPE
#endif

#endif  // FSR_CONTROLLERS__VISIBILITY_CONTROL_H_
