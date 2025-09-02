# HDA-7: End-to-End Pipeline — fMRI Connectivity Feature Extraction + Modeling

## Objective
This project implements a **reproducible end-to-end pipeline** for analyzing **resting-state fMRI** data to classify **Social Anxiety Disorder vs Control** subjects.  
The pipeline covers **data acquisition, preprocessing, feature extraction, machine learning models, evaluation, and automation**.

---

## Workflow Overview

### 1. Data Acquisition
- **Dataset**: Resting-state fMRI dataset for Social Anxiety Disorder  
- **Format**: BIDS (Brain Imaging Data Structure)  
- **Source**: [OpenNeuro](https://openneuro.org)  

---

### 2. Preprocessing
- Tool: **fMRIPrep**
- Steps:
  1. Slice-timing correction  
  2. Motion correction (realignment)  
  3. Spatial normalization to MNI space  
  4. Skull stripping  
  5. Confound regression (motion parameters, CSF, WM signals)  
- Output: Preprocessed 4D fMRI volumes per subject in MNI space  

---

### 3. Feature Extraction
- Extract **Functional Connectivity Matrices** using Pearson correlation between predefined brain regions (atlas-based parcellation).  
- **Atlas Options**: AAL, Harvard-Oxford, or custom ROI masks.  
- Pipeline:
  1. Apply brain mask and atlas to extract time series for each ROI.  
  2. Compute pairwise correlations between ROI time series.  
  3. Flatten the upper triangle of the correlation matrix into a feature vector.  

---

### 4. Secondary Dataset
- Output CSV format:  
  - **Subject_ID**: Unique identifier from the dataset  
  - **Feature_1, Feature_2, ..., Feature_N**: Flattened connectivity values  

Example:
```csv
Subject_ID,Conn_1,Conn_2,Conn_3,...
sub-01,0.45,0.23,-0.12,...
sub-02,0.51,0.19,-0.05,...
```

---

### 5. Modeling & Evaluation
- Multiple ML models implemented:
  - Logistic Regression, Random Forest, SVM  
  - Gradient Boosting (XGBoost, LightGBM, CatBoost)  
- Techniques:
  - Nested Cross-Validation  
  - Hyperparameter Tuning (GridSearchCV / Optuna)  
  - Calibration (Platt scaling, isotonic regression)  
  - Performance metrics: ROC-AUC, PR-AUC, F1, Confusion Matrix  

---

### 6. Automation Support
- Automated **update pipeline** with **watchdog**:
  - Re-runs feature extraction & modeling if new/preprocessed data is added.  
  - Saves updated CSV & model outputs automatically.  

---

## Deliverables
- `secondary_dataset.csv`: Secondary dataset with connectivity metrics  
- `fmri_pipeline.py`: End-to-end Python pipeline script  
- `requirements.txt`: Dependency list  
- `README.md`: Documentation  
- **Optional**: `environment.yml` for reproducibility with Conda  

---

## Installation

### 1. Clone repository
```bash
git clone https://github.com/VrajShah34/fmri-pipeline.git
cd fmri-pipeline
```

### 2. Create virtual environment
```bash
python -m venv venv
source venv/bin/activate   # (Linux/Mac)
venv\Scripts\activate    # (Windows)
```

### 3. Install dependencies
```bash
pip install -r requirements.txt
```

### 4. (Optional) Create Conda environment
```bash
conda env create -f environment.yml
conda activate fmri-pipeline
```

---

## Usage

### Run feature extraction + modeling pipeline
```bash
python fmri_pipeline.py --input data/preprocessed/ --output results/
```

### Watch for updates (auto-reprocessing)
```bash
python fmri_pipeline.py --watch data/preprocessed/
```

### Jupyter Notebook
```bash
jupyter notebook fmri_feature_extraction_notebook.ipynb
```

---

## Reproducibility Checklist ✅

- [ ] Python version: 3.11.x  
- [ ] Dependencies installed via `requirements.txt`  
- [ ] Dataset downloaded from [OpenNeuro](https://openneuro.org)  
- [ ] fMRIPrep preprocessing completed  
- [ ] Atlas files available (AAL / Harvard-Oxford)  
- [ ] Pipeline executed with consistent random seeds  
- [ ] Results saved in `results/` folder  

---

## References
- [fMRIPrep Documentation](https://fmriprep.org)  
- [Nilearn: Machine learning for NeuroImaging](https://nilearn.github.io)  
- [OpenNeuro Datasets](https://openneuro.org)  
