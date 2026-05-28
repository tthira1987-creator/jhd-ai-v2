# JHD Hybrid Letter™ Price Calculator — Knowledge Base
**Version:** Staff v1.0  
**System:** เส้นสี by JHD  
**Access:** PIN-protected (Staff only)  
**Purpose:** คำนวณต้นทุน + ราคาขาย ตัวอักษร Hybrid Letter

---

## METADATA

```yaml
module_id: jhd-hybrid-letter-calculator
module_type: pricing_engine
currency: THB
vat_rate: 0.07
rounding_rule: ceil_to_nearest_10
area_reference_unit: cm2
default_state:
  gradeKey: CN
  thickIdx: 2       # → 10mm
  height_cm: 30
  perim_cm: 120
  edgeKey: EDGE
  faceKey: RAW_FACE
  acpKey: PLUS
  hasDiffuser: false
  hasLED: false
  hasStandoff: false
  hasBacking: false
  qty: 1
  tierKey: retail
  showVat: false
```

---

## SECTION 1 — PLASWOOD MATERIAL (วัสดุพลาสวูด)

ราคาต่อ **ตร.ซม.** รวม VAT 7% แล้ว

### CN Series (มาตรฐาน) `badge: #38bdf8`

| ความหนา (mm) | ราคา/ตร.ซม. (฿) |
|:---:|:---:|
| 6 | 0.020 |
| 8 | 0.023 |
| 10 | 0.027 |
| 15 | 0.047 |
| 20 | 0.079 |

### TBL — Tiger Black (สีดำในตัว) `badge: #a78bfa`

| ความหนา (mm) | ราคา/ตร.ซม. (฿) |
|:---:|:---:|
| 5 | 0.022 |
| 10 | 0.029 |
| 15 | 0.061 |
| 20 | 0.068 |

### CT Series (พรีเมียม) `badge: #f0c040`

| ความหนา (mm) | ราคา/ตร.ซม. (฿) |
|:---:|:---:|
| 6 | 0.048 |
| 8 | 0.054 |
| 10 | 0.068 |
| 15 | 0.098 |
| 20 | 0.134 |

> **Lookup rule:** `matCost = height_cm² × pricePerCm2[gradeKey][thickMM]`

---

## SECTION 2 — ACP SERIES

แผ่น ACP ขนาดแผ่น = **122 × 244 cm = 29,768 ตร.ซม.**  
สูตรคำนวณ: `acpPricePerCm2 = (listPrice × 1.07) / 29768`

| ID | Name | Label | List Price (฿/แผ่น) | ราคา/ตร.ซม. (approx) | Default |
|:---|:---|:---|:---:|:---:|:---:|
| 3MM | 3MM Series | Indoor · ประหยัด | 1,000 | 0.03596 | ❌ |
| 4MM | 4MM Series | มาตรฐาน · PE Core | 1,370 | 0.04923 | ❌ |
| PLUS | PLUS Series ★ | แนะนำ · FR Core | 1,550 | 0.05570 | ✅ |
| SPECIAL | Special Surface | Luxury · พิเศษ | 1,550 | 0.05570 | ❌ |

> **ใช้เมื่อ:** `faceKey = "ACP"` → เลือก acpKey แล้วคำนวณ `faceCost = areaCm2 × acpPricePerCm2`

---

## SECTION 3 — FACE MATERIAL OPTIONS (วัสดุหน้าตัวอักษร)

| ID | Name | ราคา/ตร.ม. (฿) | หมายเหตุ |
|:---|:---|:---:|:---|
| RAW_FACE | สีพื้นวัสดุ | 0 | ไม่ทำสีหน้า ไม่ติดท็อป |
| PAINT | พ่นสี | 0 | รวมในค่าแรงเก็บขอบ (ไม่มี faceCost/glueCost) |
| ACP | ACP | (ดู Section 2) | เลือก Series ACP เพิ่มเติม |
| ZINCALU | ZincAlu | 350 | - |
| LAMINATE | ลามิเนต | 500 | - |
| ACRYLIC | อะคริลิค 3mm | 600 | - |
| WRAP | UV Print + 3M Wrap | 650 | - |

**กฎคำนวณ faceCost และ glueCost:**
- `faceKey ∈ {PAINT, RAW_FACE}` → `faceCost = 0`, `glueCost = 0`
- `faceKey = ACP` → `faceCost = areaCm2 × acpPricePerCm2(acpKey)`, `glueCost = perim × 2 × 0.50`
- `faceKey ∈ {ZINCALU, LAMINATE, ACRYLIC, WRAP}` → `faceCost = areaM2 × pricePerM2`, `glueCost = perim × 2 × 0.50`

---

## SECTION 4 — EDGE FINISHING (การเก็บขอบ)

| ID | Name | Multiplier | หมายเหตุ |
|:---|:---|:---:|:---|
| RAW | แบบดิบ | 0.25 | ไม่เก็บขอบ ไม่ทำสี |
| EDGE | โป๊วทำสีขอบ | 0.50 | เก็บขอบข้าง + ทำสีขอบ |
| FULL | พ่นสีทั้งตัว | 0.75 | โป๊ว + พ่นสีทั้งตัว |

> `edgeCost = perim_cm × edgeMult`

---

## SECTION 5 — ADD-ONS (ตัวเสริม)

### 5.1 อะคริลิครองหลัง Diffuser
- **เงื่อนไข:** `hasDiffuser = true`
- **ราคา:** 3,000 ฿/ตร.ม.
- **สูตร:** `diffuserCost = areaM2 × 3000`
- **หมายเหตุ:** กระจายแสง LED ละมุน ไม่เห็นเม็ด

### 5.2 LED Strip Halo
- **เงื่อนไข:** `hasLED = true`
- **ราคา:** 60 ฿/ม.
- **สูตร:** `ledCost = (perim_cm × 2 / 100) × 60`
- **ตัวอย่าง:** perim = 120 cm → ledCm = 240 → ledCost = 144 ฿

### 5.3 Standoff + สกรูเกลียวปล่อย
- **เงื่อนไข:** `hasStandoff = true`
- **ราคา:** 3 ฿/ตัว
- **สูตร:**
  ```
  numStandoff = ceil(height_cm / 10) × 2
  standoffCost = numStandoff × 3
  ```
- **ตัวอย่าง:** height = 30 cm → numStandoff = 6 → standoffCost = 18 ฿

### 5.4 แผ่นพื้นป้าย (Backing)
- **เงื่อนไข:** `hasBacking = true`, กำหนด `backingW` และ `backingH` (cm)
- **สูตร:** ใช้สูตรเดียวกับตัวอักษร
  ```
  backingArea = backingW × backingH   (ตร.ซม.)
  backingCost = backingArea × pricePerCm2[grade][thick]
              + (sqrt(backingArea) × 4) × 2 × 0.50    ← CNC
              + (sqrt(backingArea) × 4) × edgeMult     ← Edge
  ```
- **Default ขนาด:** กว้าง 60 cm × ยาว 150 cm

---

## SECTION 6 — SELLING PRICE TIERS (ชั้นราคา)

| Key | Label | Multiplier | หมายเหตุ |
|:---|:---|:---:|:---|
| retail | ราคาปลีก | 1.667 | ลูกค้าทั่วไป |
| partner | ช่างพาร์ทเนอร์ | 1.430 | ช่างที่ซื้อประจำ |
| dealer | ดีลเลอร์ | 1.250 | ตัวแทนจำหน่าย |

> `sellingPricePerLetter = ceil(totalCost × mult / 10) × 10`

---

## SECTION 7 — SIZE CLASSIFICATION

| Size Badge | เงื่อนไข | สี |
|:---:|:---|:---:|
| S | height ≤ 30 cm | #4ade80 (green) |
| M | 30 < height ≤ 40 cm | #f0c040 (yellow) |
| L | height > 40 cm | #f87171 (red) |

---

## SECTION 8 — CORE CALCULATION ENGINE

```
INPUT:
  gradeKey    : "CN" | "TBL" | "CT"
  thickIdx    : index ใน grade.items[]
  height_cm   : ความสูงตัวอักษร (cm)
  perim_cm    : เส้นรอบรูปตัวอักษร (cm)
  edgeKey     : "RAW" | "EDGE" | "FULL"
  faceKey     : "RAW_FACE" | "PAINT" | "ACP" | "ZINCALU" | "LAMINATE" | "ACRYLIC" | "WRAP"
  acpKey      : "3MM" | "4MM" | "PLUS" | "SPECIAL"  (ใช้เมื่อ faceKey="ACP")
  hasDiffuser : boolean
  hasLED      : boolean
  hasStandoff : boolean
  hasBacking  : boolean
  backingW    : cm (ใช้เมื่อ hasBacking=true)
  backingH    : cm (ใช้เมื่อ hasBacking=true)

INTERMEDIATE:
  areaCm2 = height² 
  areaM2  = areaCm2 / 10000
  pricePerCm2 = PLASWOOD[gradeKey].items[thickIdx].pricePerCm2

COST COMPONENTS (per 1 letter):
  1. matCost      = areaCm2 × pricePerCm2
  2. cncCost      = perim × 2 × 0.50
  3. edgeCost     = perim × edgeMult
  4. glueCost     = (faceKey ∉ {PAINT,RAW_FACE}) ? perim × 2 × 0.50 : 0
  5. faceCost     = (see Section 3)
  6. diffuserCost = hasDiffuser ? areaM2 × 3000 : 0
  7. ledCost      = hasLED ? (perim×2/100) × 60 : 0
  8. standoffCost = hasStandoff ? ceil(height/10)×2 × 3 : 0
  9. backingCost  = hasBacking ? (formula Section 5.4) : 0

  totalCost = sum(1..9)

OUTPUT:
  sellingPrice  = ceil(totalCost × tierMult / 10) × 10    ← per letter
  subtotal      = sellingPrice × qty
  vatAmt        = round(subtotal × 0.07)
  grandTotal    = subtotal + vatAmt
```

---

## SECTION 9 — QUICK REFERENCE: ตัวอย่างการคำนวณ

**Case:** ตัวอักษร CN 10mm, สูง 30cm, เส้นรอบรูป 120cm, EDGE, RAW_FACE, ไม่มี add-on, 5 ตัว, retail

```
areaCm2     = 30² = 900
areaM2      = 0.09
pricePerCm2 = 0.027

matCost     = 900 × 0.027   = 24.30 ฿
cncCost     = 120 × 2 × 0.5 = 120.00 ฿
edgeCost    = 120 × 0.50    = 60.00 ฿
glueCost    = 0
faceCost    = 0
others      = 0

totalCost   = 204.30 ฿
sellingPrice (retail) = ceil(204.30 × 1.667 / 10) × 10
                     = ceil(340.5 / 10) × 10
                     = 35 × 10 = 350 ฿/ตัว

subtotal (5ตัว)  = 350 × 5 = 1,750 ฿
+VAT 7%          = 1,750 × 1.07 = 1,872.50 ฿
```

---

## SECTION 10 — AGENT INSTRUCTIONS

> **สำหรับ AI/Sub Agent ที่ใช้ไฟล์นี้:**

### วิธีตอบคำถาม "ราคาเท่าไหร่?"

1. **รับ parameter** จากผู้ใช้: grade, ความหนา, ความสูง, เส้นรอบรูป, edge, face, add-on, จำนวน, tier
2. **Lookup ราคาวัสดุ** จาก Section 1 หรือ 2
3. **คำนวณทีละ component** ตาม Section 8
4. **ปัดขึ้น** ทุก 10 บาท
5. **แสดงผล** breakdown + ราคาสุดท้าย

### Parameter ที่ต้องถามถ้าไม่ได้รับ

| Parameter | ถามว่า | Default ถ้าไม่ตอบ |
|:---|:---|:---|
| gradeKey | ใช้พลาสวูดเกรดอะไร? (CN/TBL/CT) | CN |
| thickMM | ความหนา? | 10mm |
| height_cm | ความสูงตัวอักษร? | 30 cm |
| perim_cm | เส้นรอบรูป? | 120 cm |
| edgeKey | การเก็บขอบ? | EDGE |
| faceKey | วัสดุหน้า? | RAW_FACE |
| qty | จำนวนตัวอักษร? | 1 |
| tierKey | ชั้นราคา? (retail/partner/dealer) | retail |

### การแจ้งราคาลูกค้า

- **retail** = ลูกค้าทั่วไป → แจ้งราคาปลีก
- **partner** = ช่างที่สั่งซื้อประจำ → ใช้ tier partner
- **dealer** = ตัวแทน → ใช้ tier dealer
- ถ้าลูกค้าถามว่า "แพงไป" → แสดง tier เปรียบเทียบ 3 ชั้น
- VAT: บวกได้เมื่อลูกค้าต้องการใบกำกับภาษี (`vatAmt = subtotal × 0.07`)

---

## SECTION 11 — VALIDATION RULES

```
height_cm   : int, min=5, max=200
perim_cm    : int, min=10, ค่าแนะนำ ≈ height×4 (สี่เหลี่ยม) หรือ height×π (วงกลม)
qty         : int, min=1
backingW    : int, min=1 (เมื่อ hasBacking=true)
backingH    : int, min=1 (เมื่อ hasBacking=true)
thickIdx    : 0-based index ตาม grade.items ของ grade ที่เลือก
```

---

*ไฟล์นี้สร้างจาก jhd-hybrid-letter-calculator.jsx · เส้นสี by JHD · Staff v1.0*