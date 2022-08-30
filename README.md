# Prepare container images to build RPM files from specs or sources

## Usage

1. Building for Centos 7

```bash
cd <directory-with-a-spec-file>
make -f <path-to-this-directory>/Makefile build7
```

2. Building for Centos Stream 8
```bash
cd <directory-with-a-spec-file>
make -f <path-to-this-directory>/Makefile build8
```

3. Running Centos Stream 8 container

```bash
make Makefile run8
```
