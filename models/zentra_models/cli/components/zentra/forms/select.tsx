import { SelectItemType } from "./types";

import styles from "./form.module.css";

type SelectDataProps = {
  data: SelectItemType[];
};

type SelectArrayProps = {
  data: string[];
};

export const SelectObjData = ({
  data,
}: SelectDataProps) => {
  return data.map((item: SelectItemType) => (
    <SelectItem key={item.name} value={item.name}>
      <div className={styles.selectItemContainer}>
        {item.imgUrl && (
          <Image
            src={item.imgUrl}
            width={32}
            height={32}
            alt={item.name}
            className={styles.selectItemImage}
          />
        )}
        <p>{item.name}</p>
      </div>
    </SelectItem>
  ));
};

export const SelectStrArrayData = ({
  data,
}: SelectArrayProps) => {
  return data.map((item) => (
    <SelectItem key={item} value={item}>
      {item}
    </SelectItem>
  ));
};
