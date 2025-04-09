import React, { useState } from 'react';
import { Card, CardContent } from '@/components/ui/card';
import { Input } from '@/components/ui/input';
import { Button } from '@/components/ui/button';

export default function NomikaiBudgetSplitter() {
  const [total, setTotal] = useState(0);
  const [people, setPeople] = useState([{ name: '', amount: 0 }]);

  const handlePersonChange = (index, field, value) => {
    const newPeople = [...people];
    newPeople[index][field] = field === 'amount' ? parseInt(value || 0, 10) : value;
    setPeople(newPeople);
  };

  const addPerson = () => {
    setPeople([...people, { name: '', amount: 0 }]);
  };

  const removePerson = (index) => {
    const newPeople = people.filter((_, i) => i !== index);
    setPeople(newPeople);
  };

  const totalAssigned = people.reduce((sum, p) => sum + (p.amount || 0), 0);
  const remaining = total - totalAssigned;
  const evenSplit = total > 0 ? Math.floor(total / people.length) : 0;

  const autoAssignEven = () => {
    setPeople(people.map((p) => ({ ...p, amount: evenSplit })));
  };

  return (
    <div className="max-w-3xl mx-auto p-4 space-y-6">
      <Card>
        <CardContent className="space-y-4 p-4">
          <h2 className="text-xl font-bold">飲み会割り勘ツール</h2>
          <div>
            <label className="block text-sm font-medium">総額</label>
            <Input
              type="number"
              value={total}
              onChange={(e) => setTotal(parseInt(e.target.value || 0, 10))}
            />
          </div>

          {people.map((person, index) => (
            <div key={index} className="grid grid-cols-3 gap-2 items-center">
              <Input
                placeholder="名前"
                value={person.name}
                onChange={(e) => handlePersonChange(index, 'name', e.target.value)}
              />
              <Input
                type="number"
                placeholder="金額"
                value={person.amount}
                onChange={(e) => handlePersonChange(index, 'amount', e.target.value)}
              />
              <Button variant="outline" onClick={() => removePerson(index)}>
                削除
              </Button>
            </div>
          ))}

          <div className="flex gap-2">
            <Button onClick={addPerson}>参加者を追加</Button>
            <Button variant="secondary" onClick={autoAssignEven}>均等に割り振る</Button>
          </div>

          <div className="text-sm text-gray-700">
            割り振られた合計: {totalAssigned} 円 / 残り: {remaining} 円
          </div>
        </CardContent>
      </Card>
    </div>
  );
}